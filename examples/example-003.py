#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

b0 = Box(x=4,y=4,z=4, center=True)
s0 = Sphere(radius=2.5)

u = s0 - b0

u.toSTL(stlfname)
