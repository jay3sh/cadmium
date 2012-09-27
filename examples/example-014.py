
import sys
sys.path.append('./src')
from cadmium import Extrusion
from cadmium import CadmiumException

s = Extrusion(
      knotVector=[0,0,0,0,1,5,6,8,8,8,8],
      controlPoints=[
        [0,1,0],
        [0,1.5,0],
        [0,2,1],
        [0,3,2],
        [0,4,2.5],
        [0,1,3],
        [0,0.5,4]
      ],
      degree=3)

s.toSTL(sys.argv[1])

try:
  s = Extrusion(
      knotVector = [0,0,0,0,1,2,2,2,2],
      controlPoints = [
        [0.23750000000000002,0.4,0], 
        [4.01625,1.48,0], 
        [2.375,3.6,0],
        [0.9337500000000003,1.55,0],
        [4.5125,0.3999999999999999,0]
      ],
      degree=3)
except CadmiumException, ce:
  print "Self intersection detection worked"
