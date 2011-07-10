#!/usr/bin/python

import os
import sys
import math
sys.path.append('./src')

from cadmium import *
jsonfname = sys.argv[1]

t = Torus(r1=10,r2=2)

precision = 0.01
t.toJSON(jsonfname,compress=True,precision=precision)
size = os.stat(jsonfname).st_size
print size,precision

while size > 40*1024 and precision <= 0.1: # 40k
  os.remove(jsonfname)

  precision += 0.01
  t = Torus(r1=10,r2=2)
  t.toJSON(jsonfname, precision=precision)

  size = os.stat(jsonfname).st_size
  print size,precision
  

