# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

from OCC.BRepPrimAPI import *

from cadmium.solid import Solid

class Box(Solid):
  
  def __init__(self, x=10, y=10, z=10, center=False):
    self.instance = BRepPrimAPI_MakeBox(x,y,z)
    Solid.__init__(self, self.instance.Shape(), center=center)
    
