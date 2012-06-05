
#!/usr/bin/python

import sys
import math
sys.path.append('./src')

from cadmium import *

def main():
  solids = [
    TaperedPipePie(),
    TaperedPipePie().translate(x=2,y=2),
    TaperedPipePie().translate(x=2,z=2),
    TaperedPipePie().translate(y=2,z=2),
    TaperedPipePie().translate(x=4,y=4),
    TaperedPipePie().translate(x=4,z=4),
    TaperedPipePie().translate(y=4,z=4),
    TaperedPipePie().translate(x=6,y=6),
    TaperedPipePie().translate(x=6,z=6),
    TaperedPipePie().translate(y=6,z=6),
    TaperedPipePie().translate(x=8,y=8),
    TaperedPipePie().translate(x=8,z=8),
    TaperedPipePie().translate(y=8,z=8),
  ]

  u = reduce(lambda x,y: x+y, solids)
  u.toSTL(sys.argv[1])


class TaperedPipePie(Solid):
  def __init__(self, roTop=2, riTop=1, roBottom=4, riBottom=3, length=5, angle=120):
    if riTop >= roTop or riBottom >= roBottom:
      raise CadmiumException('Inner radius should be smaller than Outer radius')
    ro = max(roTop, roBottom)
    hr = ro*(1-math.cos((angle/2)*math.pi/180))
    s = Cylinder(r1=roTop, r2=roBottom, h=length, center=True) - \
    	Cylinder(r1=riTop, r2=riBottom, h=length, center=True)
    s -= Box(x=2*ro,y=2*ro,z=length,center=True).translate(x=2*ro-hr)
    s.rotate(axis=X_axis, angle=90)
    Solid.__init__(self, s)

if __name__ == '__main__':
  import cProfile
  cProfile.run('main()','test')
