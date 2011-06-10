#!/usr/bin/python

#
# This is a failing examples.
# It is found to consume lot of CPU and occupy lot of memory
# leading to a system crash.
#

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

b0 = Box(x=2,y=2,z=2)

s0 = Sphere(radius=2)

u = s0 - b0

u.toSTL(stlfname)
