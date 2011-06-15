# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

#!/usr/bin/python

import math
import cadmium

from OCC import StlAPI
from OCC.BRepAlgoAPI import *
from OCC.BRepBuilderAPI import *
from OCC.gp import *
import OCC.TopoDS

class Solid():
  def __init__(self, s=None):
    if type(s) == OCC.TopoDS.TopoDS_Shape:
      self.shape = s
    else:
      self.shape = s.shape

  def __add__(self, other):
    union = BRepAlgoAPI_Fuse(self.shape, other.shape).Shape()
    return Solid(union)

  def __mul__(self, other):
    intersection = BRepAlgoAPI_Common(self.shape, other.shape).Shape()
    return Solid(intersection)

  def __sub__(self, other):
    subtraction = BRepAlgoAPI_Cut(self.shape, other.shape).Shape()
    return Solid(subtraction)

  def center(self):
    '''
    Returns center of the polyhedron

    This algo must take into consideration the initial center adjustment
    if one was done. This adjustment is done in the constructor of 
    primitive, based on its dimensions
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
    if x != 0 or y != 0 or z != 0:
      delta = [x,y,z]

    xform = gp_Trsf()
    xform.SetTranslation(gp_Vec(delta[0], delta[1], delta[2]))
    brep = BRepBuilderAPI_Transform(self.shape, xform, False)
    brep.Build()
    self.shape = brep.Shape()
    return self

  def rotate(self, axis=cadmium.Z_axis, angle=0):
    xform = gp_Trsf()
    xform.SetRotation(axis, angle*math.pi/180.0);
    brep = BRepBuilderAPI_Transform(self.shape, xform, False)
    brep.Build()
    self.shape = brep.Shape()
    return self

  def scale(self, scale=1, reference=None):
    if not reference: reference = self.center()
    xform = gp_Trsf()
    xform.SetScale(reference, scale);
    brep = BRepBuilderAPI_Transform(self.shape, xform, False)
    brep.Build()
    self.shape = brep.Shape()
    return self

  def toSTL(self, filename, ascii=False):
    StlAPI.StlAPI_Write(self.shape, filename, ascii)
