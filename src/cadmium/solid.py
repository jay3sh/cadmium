# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

#!/usr/bin/python

import os
from math import pi as math_pi
import cadmium
import json

from OCC import StlAPI
from OCC.BRepAlgoAPI import *
from OCC.BRepBuilderAPI import *
from OCC.gp import *
from OCC import Bnd, BRepBndLib

from OCC.Utils.Topology import *
from OCC.TopoDS import *
from OCC.TopAbs import *

# For generating Triangle Mesh
from OCC.BRepMesh import *
from OCC.BRep import *
from OCC.BRepTools import BRepTools

from OCC.Precision import *

class Solid():
  '''
  Base class for all solids (Primitive and Custom). It's created by passing in Shape as argument.
  '''
  def __init__(self, s=None, center=False):
    if s:
      if type(s) == TopoDS_Shape:
        self.shape = s
      else:
        self.shape = s.shape
    else:
      self.shape = TopoDS_Shape()

    self.centerTranslation = [0,0,0]
    if center: self.centralize()

  def __add__(self, other):
    '''
    **Union** with other solid.
    '''
    union = BRepAlgoAPI_Fuse(self.shape, other.shape).Shape()
    return Solid(union)

  def __mul__(self, other):
    '''
    **Intersect** with other solid
    '''
    intersection = BRepAlgoAPI_Common(self.shape, other.shape).Shape()
    return Solid(intersection)

  def __sub__(self, other):
    '''
    **Subtract** other solid from this
    '''
    subtraction = BRepAlgoAPI_Cut(self.shape, other.shape).Shape()
    return Solid(subtraction)

  def _triangle_is_valid(self, P1,P2,P3):
      ''' check wether a triangle is or not valid
      '''
      V1 = gp_Vec(P1,P2)
      V2 = gp_Vec(P2,P3)
      V3 = gp_Vec(P3,P1)
      if V1.SquareMagnitude()>1e-10 and V2.SquareMagnitude()>1e-10 and V3.SquareMagnitude()>1e-10:
          V1.Cross(V2)
          if V1.SquareMagnitude()>1e-10:
              return True
          else:
              print 'Not valid!'
              return False
      else:
          print 'Not valid!'
          return False

  def getBoundingBox(self):
    '''
    Returns Bounding Box of this solid

    The bounds are returns in an array [xmin, ymin, zmin, xmax, ymax, zmax]
    '''
    box = Bnd.Bnd_Box();
    b = BRepBndLib.BRepBndLib();
    b.Add(self.shape, box);
    return box.Get()

  def centralize(self):
    xmin, ymin, zmin, xmax, ymax, zmax = self.getBoundingBox()
    xspan = xmax - xmin
    yspan = ymax - ymin
    zspan = zmax - zmin
    self.centerTranslation = \
      ((-xspan/2.)-xmin, (-yspan/2.)-ymin, (-zspan/2.)-zmin)
    self.translate(delta=self.centerTranslation)

  def _vtxkey(self, v):
    return '%.4f_%.4f_%.4f'%(v[0], v[1], v[2])

  def _save_vertex(self, vertex):
    key = self._vtxkey(vertex)
    if self.vtxmap.has_key(key):
      return self.vtxmap[key]
    else:
      self.vtxmap[key] = self.vcount
      self.vertices.append(vertex)
      self.vcount += 1
      return self.vcount-1

  def _save_face(self, indices):
    self.faces.append(indices)

  def _reset_mesh(self):
    self.vtxmap = {}
    self.vcount = 0
    self.faces = []
    self.vertices = []

  def _compress_write(self, filename):
    vstr = '['+','.join(map(lambda x: '[%.2f,%.2f,%.2f]'%\
      (x[0],x[1],x[2]), self.vertices))+']'
    fstr = '['+','.join(map(lambda x: '[%d,%d,%d]'%\
      (x[0],x[1],x[2]), self.faces))+']'
    minjson = '{"vertices":'+vstr+',"faces":'+fstr+'}'

    plain = open(filename+'.plain', 'w')
    plain.write(minjson)
    plain.close()
    plain = open(filename+'.plain','rb')

    import gzip
    compressed = gzip.open(filename, 'wb')
    compressed.writelines(plain)
    compressed.close()
    os.remove(filename+'.plain')

  def _build_mesh(self, precision=0.01):
    self._reset_mesh()
    BRepMesh_Mesh(self.shape, precision)
    faces_iterator = Topo(self.shape).faces()

    for F in faces_iterator:
      face_location = F.Location()
      facing = BRep_Tool_Triangulation(F,face_location).GetObject()
      tab = facing.Nodes()
      tri = facing.Triangles()

      for i in range(1,facing.NbTriangles()+1):
        trian = tri.Value(i)
        if F.Orientation() == TopAbs_REVERSED:
          index1, index3, index2 = trian.Get()
        else:
          index1, index2, index3 = trian.Get()
        P1 = tab.Value(index1).Transformed(face_location.Transformation())
        P2 = tab.Value(index2).Transformed(face_location.Transformation())
        P3 = tab.Value(index3).Transformed(face_location.Transformation())

        p1_coord = P1.XYZ().Coord()
        p2_coord = P2.XYZ().Coord()
        p3_coord = P3.XYZ().Coord()

        if self._triangle_is_valid(P1, P2, P3):
          i1 = self._save_vertex(p1_coord)
          i2 = self._save_vertex(p2_coord)
          i3 = self._save_vertex(p3_coord)
          self._save_face([i1,i2,i3])

  def getMesh(self, precision=0.01):
    self._build_mesh(precision)
    return { 'vertices':self.vertices, 'faces':self.faces }

  def toJSON(self, filename, compress=False, precision=0.01):
    '''
    Writes JSON representation of the mesh

    :param filename: Path of the file to write JSON to
    :type filename: str
    :param precision: Provides control over quality of exported mesh. Higher the precision value, lower the accuracy of exported mesh, smaller the size of exported file. Lower the precision value, more accurate the exported mesh, bigger the size of exported file.
    :type precision: float
    '''
    self._build_mesh(precision)

    if compress:
      self._compress_write(filename)
    else:
      open(filename, 'w').write(json.dumps({
        'vertices':self.vertices,'faces':self.faces}))


  def center(self):
    '''
    Returns center of the solid

    This algo takes into consideration the initial center adjustment 
    (if one was done). This adjustment is done in the constructor 
    of primitive, based on its dimensions
    '''
    center = gp_Pnt(0,0,0)

    if self.centerTranslation:
      ct = self.centerTranslation
      minus_ct = (-ct[0], -ct[1], -ct[2])
      minusCenterTranslation = gp_Trsf()
      minusCenterTranslation.SetTranslation(
        gp_Vec(minus_ct[0],minus_ct[1],minus_ct[2]))
      center.Transform(minusCenterTranslation)

    xform = self.shape.Location().Transformation()
    center.Transform(xform)
    return center
     
  def translate(self, x=0, y=0, z=0, delta=[0,0,0]):
    '''
    Translate the solid.
    Either provide delta or one of x,y,z. If either x,y or z are non-zero,
    delta will be ignored.

    :param delta: Translation vector
    :type delta: float
    :param x: Translation along X
    :type x: float
    :param y: Translation along Y
    :type y: float
    :param z: Translation along Z
    :type z: float
    '''
    if x != 0 or y != 0 or z != 0:
      delta = [x,y,z]

    xform = gp_Trsf()
    xform.SetTranslation(gp_Vec(delta[0], delta[1], delta[2]))
    brep = BRepBuilderAPI_Transform(self.shape, xform, False)
    brep.Build()
    self.shape = brep.Shape()
    return self

  def rotate(self, axis=cadmium.Z_axis, angle=0):
    '''
    Rotate the solid

    :param axis: One of three principal axes (cadmium.X_axis, cadmium.Y_axis, cadmium.Z_Axis)
    :param angle: in Degrees
    :type angle: float
    '''
    xform = gp_Trsf()
    xform.SetRotation(axis, angle*math_pi/180.0);
    brep = BRepBuilderAPI_Transform(self.shape, xform, False)
    brep.Build()
    self.shape = brep.Shape()
    return self

  def scale(self, scale=1, scaleX=1, scaleY=1, scaleZ=1):
    '''
    Scale the solid. Either provide scale parameter for uniform scaling along 
    all axis. If scale is not provided, but one of scaleX,scaleY,scaleZ is 
    provided, the solid is scaled along respective dimensions.

    :param scale: Uniform scale factor along all dimensions
    :type scale: float
    :param scaleX: Scale factor along X
    :type scaleX: float
    :param scaleY: Scale factor along Y
    :type scaleY: float
    :param scaleZ: Scale factor along Z
    :type scaleZ: float
    '''
    if scale != 1:
      scaleX = scaleY = scaleZ = scale

    xform = gp_GTrsf()
    xform.SetVectorialPart(gp_Mat(
      scaleX, 0, 0,
      0, scaleY, 0,
      0, 0, scaleZ,
    ))
    brep = BRepBuilderAPI_GTransform(self.shape, xform, False)
    brep.Build()
    self.shape = brep.Shape()
    return self

  def shear(self, xy=0, xz=0, yx=0, yz=0, zx=0, zy=0):
    '''
    Shear the solid

    :param xy: Shear along X-axis as function of y
    :type xy: float
    :param xz: Shear along X-axis as function of z
    :type xz: float
    :param yx: Shear along Y-axis as function of x
    :type yx: float
    :param yz: Shear along Y-axis as function of z
    :type yz: float
    :param zx: Shear along Z-axis as function of x
    :type zx: float
    :param zy: Shear along Z-axis as function of y
    :type zy: float
    '''
    xform = gp_Trsf()
    xform.SetValues(
      1, xy, xz, 0,
      yx, 1, yz, 0,
      zx, zy, 1, 0,
      Precision_Angular(), Precision_Confusion()
    );
    brep = BRepBuilderAPI_GTransform(self.shape, gp_GTrsf(xform), False)
    brep.Build()
    self.shape = brep.Shape()
    return self

  def toSTL(self, filename, ascii=False, deflection=0.01):
    '''
    Writes STL output of the solid

    :param filename: Path of the file to write JSON to
    :type filename: str
    :param ascii: choose between ASCII or Binary STL format
    :type ascii: bool
    :param deflection: Provides control over quality of exported STL. Higher the deflection value, lower the accuracy of exported STL, smaller the size of resulting file. Lower the deflection value, more accurate the exported STL, bigger the size of resulting file.
    :type deflection: float
    '''
    stl_writer = StlAPI.StlAPI_Writer()
    stl_writer.SetASCIIMode(ascii)
    stl_writer.SetDeflection(deflection)
    stl_writer.Write(self.shape, filename)

  def toBREP(self, filename):
    '''
    Write BREP output of the solid

    :param filename: Path of the file to write BREP to
    '''
    BRepTools().Write(self.shape, filename)

  def fromBREP(self, filename):
    '''
    Load ths solid from BREP file

    :param filename: Path of the file to read BREP from
    '''
    BRepTools().Read(self.shape, filename, BRep_Builder())
