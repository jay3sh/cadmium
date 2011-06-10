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

class Polyhedron():
  def __init__(self, shape=None):
    self.shape = shape

  def __add__(self, other):
    union = BRepAlgoAPI_Fuse(self.shape, other.shape).Shape()
    return Polyhedron(shape=union)

  def __mul__(self, other):
    intersection = BRepAlgoAPI_Common(self.shape, other.shape).Shape()
    return Polyhedron(shape=intersection)

  def __sub__(self, other):
    subtraction = BRepAlgoAPI_Cut(self.shape, other.shape).Shape()
    return Polyhedron(shape=subtraction)

  def translate(self, x=0, y=0, z=0, delta=[0,0,0]):
    if x > 0 or y > 0 or z > 0:
      delta = [x,y,z]

    xform = gp_Trsf()
    xform.SetTranslation(gp_Vec(delta[0], delta[1], delta[2]))
    brep = BRepBuilderAPI_Transform(self.shape, xform, False)
    brep.Build()
    self.shape = brep.Shape()

  def rotate(self, axis=cadmium.Z_axis, angle=0):
    xform = gp_Trsf()
    xform.SetRotation(axis, angle*math.pi/180.0);
    brep = BRepBuilderAPI_Transform(self.shape, xform, False)
    brep.Build()
    self.shape = brep.Shape()

  def toSTL(self, filename, ascii=False):
    StlAPI.StlAPI_Write(self.shape, filename, ascii)
