# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.polyhedron import Polyhedron

class Wedge(Polyhedron):
  
  def __init__(self, dx=5, dy=5, dz=5, ltx=0):
    self.instance = BRepPrimAPI_MakeWedge(dx, dy, dz, ltx)
    Polyhedron.__init__(self, shape=self.instance.Shape())
    
