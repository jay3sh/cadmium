# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

from OCC.BRepPrimAPI import *

from cadmium.polyhedronOCC import Polyhedron

class Box(Polyhedron):
  
  def __init__(self, x=10, y=10, z=10):
    self.instance = BRepPrimAPI_MakeBox(x,y,z)
    Polyhedron.__init__(self, shape=self.instance.Shape())
    
