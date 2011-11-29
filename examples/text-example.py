
#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

stlfname = sys.argv[1]

s = Text('Cadmium',
  fontpath='DejaVuSerif.ttf', # Give full path on your system
  height=5,
  thickness=2)

s.toSTL(stlfname)
