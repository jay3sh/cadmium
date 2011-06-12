#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

def dragon(k,s):
  if k < 1:
    return Cylinder(r=2*s, h=1).scale(0.1).translate(x=s) + \
      Box(x=s, y=2*s/5.0, z=1).translate(y=-s/5.0) + \
      Cylinder(r=2*s, h=1).scale(0.1)
  else:
    c = pow(complex(1, -1), k)
    return dragon(k-1,s) +\
      dragon(k-1,s).rotate(Z_axis, 90).translate(x=c.real,y=c.imag)

print 'This is going to take a while...'
u = dragon(8,1)

u.toSTL(stlfname)
