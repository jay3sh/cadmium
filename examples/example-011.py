#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *
stlfname = sys.argv[1]

t = Torus(r1=10,r2=2)

t.toSTL(stlfname)

