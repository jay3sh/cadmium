#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

b = Box(x=2,y=2,z=2,center=True)
s = Sphere(r=0.5).translate(0,1,0)

u = b-s

u.toSTL(stlfname)
