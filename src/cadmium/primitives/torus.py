# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.solid import Solid

class Torus(Solid):
  
  def __init__(self, r1=None, r2=None, angle=360, center=False):
    self.instance = BRepPrimAPI_MakeTorus(r1,r2,angle*math.pi/180)
    Solid.__init__(self, self.instance.Shape())
