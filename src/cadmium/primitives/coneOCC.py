# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.polyhedronOCC import Polyhedron

class Cone(Polyhedron):
  
  def __init__(self, radius1=5, radius2=5, height=10, pie=360):
    self.instance = BRepPrimAPI_MakeCone(
      radius1, radius2, height, pie*math.pi/180)
    Polyhedron.__init__(self, shape=self.instance.Shape())
    
