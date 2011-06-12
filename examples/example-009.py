#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *
stlfname = sys.argv[1]

LIMIT = 9

def count_zeroes(lst):
 return sum(1 for x in lst if x == 0)

def menger_void(k):
  core = Box(k/3,k/3,k/3,center=True) + \
    Box(k/3,k/3,k/3,center=True).translate(0,0,k/3) + \
    Box(k/3,k/3,k/3,center=True).translate(0,k/3,0) + \
    Box(k/3,k/3,k/3,center=True).translate(k/3,0,0) + \
    Box(k/3,k/3,k/3,center=True).translate(0,0,-k/3) + \
    Box(k/3,k/3,k/3,center=True).translate(0,-k/3,0) + \
    Box(k/3,k/3,k/3,center=True).translate(-k/3,0,0)

  if k > LIMIT:
    for x in [-1,0,1]:
      for y in [-1,0,1]:
        for z in [-1,0,1]:
          if count_zeroes((x,y,z)) <= 1:
            sys.stdout.write('.')
            sys.stdout.flush()
            core += menger_void(k/3).translate(x*k/3, y*k/3, z*k/3)
  return core

print 'This will take a while...'
solid = Box(27,27,27,center=True) - menger_void(27)

solid.toSTL(stlfname)
