# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#


from OCC.gp import *
from OCC.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d
from OCC.TColStd import TColStd_Array1OfReal,TColStd_Array1OfInteger
from OCC.Geom import Geom_BezierCurve,Geom_BSplineCurve,Handle_Geom_BSplineCurve
from OCC.BRepPrimAPI import *
from OCC.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Geom import Geom_SurfaceOfRevolution
from OCC.BRepBuilderAPI import \
  BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Geom2dAPI import Geom2dAPI_InterCurveCurve
from OCC.Geom2d import Geom2d_BSplineCurve

from cadmium.solid import Solid

def unique(seq):
  noDupes = [] 
  [noDupes.append(i) for i in seq if not noDupes.count(i)] 
  return noDupes

def get_principal_plane(points):
  refx = points[0][0]
  refy = points[0][1]
  refz = points[0][2]
  if all(map(lambda x: x[0] == refx, points)): return 0
  if all(map(lambda x: x[1] == refy, points)): return 1
  if all(map(lambda x: x[2] == refz, points)): return 2
  from cadmium import CadmiumException
  raise CadmiumException('Control points not in plane')
  
def is_self_intersecting(h_curve):
  isect = Geom2dAPI_InterCurveCurve(h_curve)
  return isect.NbPoints() > 0

class Extrusion(Solid):

  def __init__(self,
    knotVector=[], controlPoints=[], degree=3, thickness=10, axis=0,
    center=False):

    self.thickness = thickness

    wire = BRepBuilderAPI_MakeWire()

    uniqueKnots = unique(knotVector)
    frequency = [ knotVector.count(knot) for knot in uniqueKnots ]

    knots = TColStd_Array1OfReal(0, len(uniqueKnots)-1)
    for i in range(len(uniqueKnots)):
      knots.SetValue(i, uniqueKnots[i])

    mults = TColStd_Array1OfInteger(0, len(frequency)-1)
    for i in range(len(frequency)):
      mults.SetValue(i,frequency[i])

    poles = TColgp_Array1OfPnt(0, len(controlPoints)-1)
    for i in range(len(controlPoints)):
      p = controlPoints[i]
      poles.SetValue(i, gp_Pnt(p[0],p[1],p[2]))

    poles2d = TColgp_Array1OfPnt2d(0, len(controlPoints)-1)
    plane = get_principal_plane(controlPoints)
    for i in range(len(controlPoints)):
      p = controlPoints[i]
      if plane == 0:
        poles2d.SetValue(i, gp_Pnt2d(p[1],p[2]))
      elif plane == 1:
        poles2d.SetValue(i, gp_Pnt2d(p[0],p[2]))
      elif plane == 2:
        poles2d.SetValue(i, gp_Pnt2d(p[0],p[1]))

    curve2d = Geom2d_BSplineCurve(poles2d, knots, mults, degree)
    if is_self_intersecting(curve2d.GetHandle()):
      from cadmium import CadmiumException
      raise CadmiumException('Self intersecting BSpline not allowed')

    curve = Geom_BSplineCurve(poles, knots, mults, degree)

    me = BRepBuilderAPI_MakeEdge(curve.GetHandle())    
    wire.Add(me.Edge())

    first = controlPoints[0]
    first = gp_Pnt(first[0], first[1], first[2])
    last = controlPoints[-1]
    last = gp_Pnt(last[0], last[1], last[2])

    if not first.IsEqual(last,1.0e-9):
      closer = BRepBuilderAPI_MakeEdge(
        gp_Lin(first,gp_Dir(gp_Vec(first,last))), first, last)
      wire.Add(closer.Edge())

    face = BRepBuilderAPI_MakeFace(wire.Wire())
    if axis == 0:
      extrusion_vector = gp_Vec(self.thickness,0,0)
    elif axis == 1:
      extrusion_vector = gp_Vec(0,self.thickness,0)
    elif axis == 2:
      extrusion_vector = gp_Vec(0,0,self.thickness)

    self.instance = BRepPrimAPI_MakePrism(face.Shape(), extrusion_vector)
    Solid.__init__(self, self.instance.Shape(), center=center)


