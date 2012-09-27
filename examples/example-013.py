
import sys
sys.path.append('./src')
from cadmium import Revolution
from cadmium import CadmiumException

s = Revolution(
      knotVector=[0,0,0,0,1,5,6,8,8,8,8],
      controlPoints=[
        [0,0,0],
        [1.5,0,0],
        [2,1,0],
        [3,2,0],
        [4,2.5,0],
        [1,3,0],
        [0,4,0]
      ],
      degree=3,
      axis=1)

s.toSTL(sys.argv[1])

try:
  s = Revolution(
    knotVector = [0,0,0,0,1,2,2,2,2],
    controlPoints = [
      [0.48,0.4,0], 
      [2.44,2.32,0],
      [4.275,2,0],
      [3.44,0.57,0],
      [0.48,3.6,0]
    ],
    degree=3)
except CadmiumException, ce:
  print "Self intersection detection worked"
