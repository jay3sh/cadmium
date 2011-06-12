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
  core = Box(k,k,k,center=True) + \
    Box(k,k,k,center=True).translate(0,0,k) + \
    Box(k,k,k,center=True).translate(0,k,0) + \
    Box(k,k,k,center=True).translate(k,0,0) + \
    Box(k,k,k,center=True).translate(0,0,-k) + \
    Box(k,k,k,center=True).translate(0,-k,0) + \
    Box(k,k,k,center=True).translate(-k,0,0)

  if 3*k > LIMIT:
    for x in [-1,0,1]:
      for y in [-1,0,1]:
        for z in [-1,0,1]:
          if count_zeroes((x,y,z)) <= 1:
            core += menger_void(k).translate(x*k, y*k, z*k)
  return core

print 'This will take a while...'
solid = Box(27,27,27,center=True) - menger_void(9)

solid.toSTL(stlfname)
