# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

from OCC.BRepPrimAPI import *

from cadmium.polyhedron import Solid

class Box(Solid):
  
  def __init__(self, x=10, y=10, z=10, center=False):

    if center:
      self.centerTranslation = (-x/2.0, -y/2.0, -z/2.0)
    else:
      self.centerTranslation = (0,0,0)

    self.instance = BRepPrimAPI_MakeBox(x,y,z)
    Solid.__init__(self, self.instance.Shape())
    self.translate(delta=self.centerTranslation)
    
