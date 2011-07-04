# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.solid import Solid

class Cone(Solid):
  
  def __init__(self, r=None, radius=None, h=None, height=None, 
    pie=360, center=False):

    if radius: r = radius
    if height: h = height

    if center:
      self.centerTranslation = (0,0,-h/2.0)
    else:
      self.centerTranslation = (0,0,0)

    self.instance = BRepPrimAPI_MakeCone(r, 0.01, h, pie*math.pi/180)
    Solid.__init__(self, self.instance.Shape())

    self.translate(delta=self.centerTranslation)
    
