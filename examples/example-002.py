#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

b1 = Box(x=4, y=4, z=4)
b1.rotate(Y_axis, 30)

b2 = Box(x=6, y=4, z=4)
b2.rotate(Z_axis, 30)

c1 = Cylinder(radius=1, height=20)
c1.rotate(X_axis, 30)
c1.translate(2,0,0)

p = (b1 + b2) - c1

p.toSTL(stlfname)
