#!/usr/bin/python

#
# This is a failing examples.
# It is found to consume lot of CPU and occupy lot of memory
# leading to a system crash.
#

import sys
import math
sys.path.append('./src')

from cadmium import Box
from cadmium import Sphere
from cadmium import Cylinder

stlfname = sys.argv[1]

b0 = Box(x=2,y=2,z=2)
c0 = Cylinder(radius=1, height=8)

s0 = Sphere(radius=2)

u = b0 + s0

fd = open(stlfname, 'w')
fd.write(u.toSTL())
fd.close()
