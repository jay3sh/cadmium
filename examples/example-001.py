#!/usr/bin/python

import sys
sys.path.append('./src')

from cadmium import Box
from cadmium import Sphere
from cadmium import Cylinder

stlfname = sys.argv[1]

b1 = Box(x=4,y=4,z=4)
b2 = Box(x=4,y=4,z=4)
b2.translate([2,2,2])

s1 = Sphere(radius=3)
s1.translate([2,3,2])

c1 = Cylinder(radius=1, height=8)
c1.translate([1,1,2])

u = b1*c1

fd = open(stlfname, 'w')
fd.write(u.toSTL())
fd.close()
