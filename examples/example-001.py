#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import Box
from cadmium import Sphere
from cadmium import Cylinder

stlfname = sys.argv[1]

c0 = Cylinder(radius=1, height=8)
c1 = Cylinder(radius=1, height=6)
c1.rotate([0,0,1], 30*math.pi/180.0)
c2 = Cylinder(radius=1, height=6)
c2.rotate([0,0,1], -30*math.pi/180.0)

b = Box(x=1,y=1,z=8)
b.translate([0.5,0.5,0])

u = (c0 + c1 + c2) - b

fd = open(stlfname, 'w')
fd.write(u.toSTL())
fd.close()
