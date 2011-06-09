# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

#!/usr/bin/python

from OCC import StlAPI
from OCC import BRepPrimAPI
from OCC.BRepAlgoAPI import *

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

  def toSTL(self, filename, ascii=False):
    StlAPI.StlAPI_Write(self.shape, filename, ascii)
