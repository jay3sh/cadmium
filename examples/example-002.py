
import sys
import math
sys.path.append('./src')

from cadmium import Box
from cadmium import Sphere
from cadmium import Cylinder

stlfname = sys.argv[1]

b1 = Box(x=4, y=4, z=4)
b1.rotate([0,1,0], 30*math.pi/180.0)

b2 = Box(x=6, y=4, z=4)
b2.rotate([0,0,1], 30*math.pi/180.0)

c1 = Cylinder(radius=1, height=5)

p = b1 + b2

fd = open(stlfname, 'w')
fd.write(p.toSTL())
fd.close()
