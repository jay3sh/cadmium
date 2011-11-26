#!/usr/bin/python

import os
import sys
import math
sys.path.append('./src')

from cadmium import *

def mem(size="rss"):
    """Generalization; memory sizes: rss, rsz, vsz."""
    return int(os.popen('ps -p %d -o %s | tail -1' %
                        (os.getpid(), size)).read())
def rss():
    """Return ps -o rss (resident) memory in kB."""
    return float(mem("rss"))/1024

print 'Initial',rss(),'Kb'

s = Box(1,1,1)
for i in range(1,100):
  s += Box(1,1,1).translate(x=i)

garbage_collect() # Comment out this line to test mem usage without GC
print 'With GC',rss(),'Kb'

