# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.solid import Solid

class Cone(Solid):
  
  def __init__(self, r=None, radius=None, h=None, height=None, pie=360):
    if radius: r = radius
    if height: h = height
    self.instance = BRepPrimAPI_MakeCone(r1, r2, h, pie*math.pi/180)
    Solid.__init__(self, self.instance.Shape())
    
