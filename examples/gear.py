#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import Box
from cadmium import Cylinder

stlfname = sys.argv[1]

c0 = Cylinder(radius=2, height=2)
c0.translate([0,-0.5,0])
c1 = Cylinder(radius=4, height=2)
c1.translate([0,-0.5,0])
ring = c1 - c0

teeth = [
  Box(x=4, y=1, z=2),
  Box(x=4, y=1, z=2),
  Box(x=2, y=1, z=4),
  Box(x=2, y=1, z=4),
  Box(x=4, y=1, z=2),
  Box(x=4, y=1, z=2),
  Box(x=2, y=1, z=4),
  Box(x=2, y=1, z=4),
]

teeth[0].translate([4,0,0])
teeth[1].translate([-4,0,0])
teeth[2].translate([0,0,4])
teeth[3].translate([0,0,-4])

teeth[4].translate([4,0,0])
teeth[4].rotate([0,1,0], 45*math.pi/180.0)

teeth[5].translate([-4,0,0])
teeth[5].rotate([0,1,0], -45*math.pi/180.0)

teeth[6].translate([0,0,4])
teeth[6].rotate([0,1,0], 45*math.pi/180.0)

teeth[7].translate([0,0,-4])
teeth[7].rotate([0,1,0], 135*math.pi/180.0)

gear = ring + reduce(lambda x,y: x+y, teeth)

fd = open(stlfname, 'w')
fd.write(gear.toSTL())
fd.close()
