# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.solid import Solid

class Wedge(Solid):
  
  def __init__(self, dx=5, dy=5, dz=5, center=True, ltx=0):
    if center:
      self.centerTranslation = (0,-dy/2.0,0)
    else:
      self.centerTranslation = (0,0,0)

    self.instance = BRepPrimAPI_MakeWedge(dx, dy, dz, ltx)
    Solid.__init__(self, self.instance.Shape())

    self.translate(delta=self.centerTranslation)
    
