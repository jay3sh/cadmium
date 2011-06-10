# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.polyhedronOCC import Polyhedron

class Cylinder(Polyhedron):
  
  def __init__(self, radius=5, height=10, pie=360, center=False):
    self.instance = BRepPrimAPI_MakeCylinder(
      radius, height, pie*math.pi/180)
    Polyhedron.__init__(self, shape=self.instance.Shape())
    if center: self.translate(0,0,-height/2.0)
    
