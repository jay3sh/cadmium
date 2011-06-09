# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math
from OCC.BRepPrimAPI import *

from cadmium.polyhedronOCC import Polyhedron

class Sphere(Polyhedron):
  
  def __init__(self, radius=5, phi=360):
    self.instance = BRepPrimAPI_MakeSphere(radius, phi*math.pi/180)
    Polyhedron.__init__(self, shape=self.instance.Shape())
