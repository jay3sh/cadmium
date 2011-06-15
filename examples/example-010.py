#!/usr/bin/python

#
# Spoked Wheel
# Demonstrates use of Object Oriented python for Solid modelling
#

import sys
import math
sys.path.append('./src')

from cadmium import *
stlfname = sys.argv[1]

class Spoke(Solid):
  def __init__(self, maxr, smallr, bigr, height, ratio, center=True):
    short_h = ratio * height
    long_h = height - short_h

    solid = Cylinder(r1=smallr,r2=maxr,h=long_h,center=True).translate(z=-long_h/2) +\
            Cylinder(r1=maxr,r2=bigr,h=short_h,center=True).translate(z=short_h/2)
    if center: solid.translate(z=(height/2 - short_h))
    Solid.__init__(self, solid)

wheel_outer_dia = 40
wheel_thickness = 4
num = 8
spokes = map(
  lambda i: Spoke(maxr=1.5, smallr=1, bigr=1.2, height=
              (wheel_outer_dia/2-wheel_thickness/2), ratio=0.3)
            .translate(z=-10)
            .rotate(X_axis, i*360/num),
  range(num))

rim = Cylinder(r=wheel_outer_dia/2,h=4,center=True)-\
      Cylinder(r=(wheel_outer_dia-wheel_thickness)/2,h=4,center=True)-\
      Cylinder(r=((wheel_outer_dia-wheel_thickness)/2)+0.5,h=2,center=True)
rim.rotate(Y_axis, 90)

axel = Cylinder(r=3.5,h=3,center=True).rotate(Y_axis, 90)
hole = Cylinder(r=2,h=3,center=True).rotate(Y_axis, 90)

solid = (reduce(lambda x,y: x+y, spokes) + axel - hole) + rim

solid.toSTL(stlfname)
