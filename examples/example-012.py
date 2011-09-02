#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

s = Sphere(r=3)
s.scale(scaleY=2, scaleZ=2)

s.toSTL(stlfname)
