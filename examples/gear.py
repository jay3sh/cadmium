#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

ring = (
  Cylinder(radius=6, height=2, center=True) - \
  Cylinder(radius=4, height=2, center=True)).rotate(Y_axis, 90)

cogs = [
  Box(1,1,5, center=True).rotate(X_axis, 135).translate(0,5,5),
  Box(1,1,5, center=True).rotate(X_axis, -135).translate(0,5,-5),
  Box(1,1,5, center=True).rotate(X_axis, 45).translate(0,-5,5),
  Box(1,1,5, center=True).rotate(X_axis, -45).translate(0,-5,-5),
  Box(1,1,5, center=True).rotate(X_axis, 90).translate(0,5*math.sqrt(2),0),
  Box(1,1,5, center=True).rotate(X_axis, 90).translate(0,-5*math.sqrt(2),0),
  Box(1,1,5, center=True).translate(0,0,5*math.sqrt(2)),
  Box(1,1,5, center=True).translate(0,0,-5*math.sqrt(2)),
]

gear = ring + reduce(lambda x,y: x+y, cogs)

gear.toSTL(stlfname)
