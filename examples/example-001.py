#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

c0 = Cylinder(radius=1, height=8)
c1 = Cylinder(radius=1, height=6)
c1.rotate(X_axis, 30)
c2 = Cylinder(radius=1, height=6)
c2.rotate(X_axis, -30)

b = Box(x=1,y=5,z=1)
b.translate(0,-2.5,3)

u = (c0 + c1 + c2) - b

u.toSTL(stlfname)
