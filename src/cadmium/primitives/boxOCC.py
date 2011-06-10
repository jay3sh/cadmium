# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

from OCC.BRepPrimAPI import *

from cadmium.polyhedronOCC import Polyhedron

class Box(Polyhedron):
  
  def __init__(self, x=10, y=10, z=10, center=False):
    self.instance = BRepPrimAPI_MakeBox(x,y,z)
    Polyhedron.__init__(self, shape=self.instance.Shape())
    if center: self.translate(-x/2.0, -y/2.0, -z/2.0)
    
