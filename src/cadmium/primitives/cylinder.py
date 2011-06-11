# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.polyhedron import Polyhedron

class Cylinder(Polyhedron):
  
  def __init__(self, r=None, radius=None, r1=None, r2=None, height=None, 
    h=None, pie=360, center=False):

    if radius: r=radius
    if height: h=height

    if r1 != r2:
      self.instance = BRepPrimAPI_MakeCone(r1, r2, h, pie*math.pi/180)
      Polyhedron.__init__(self, shape=self.instance.Shape())
      if center: self.translate(0,0,-h/2.0)
    else:
      if not r: r = r1 = r2
      self.instance = BRepPrimAPI_MakeCylinder(r, h, pie*math.pi/180)
      Polyhedron.__init__(self, shape=self.instance.Shape())
      if center: self.translate(0,0,-h/2.0)
    
