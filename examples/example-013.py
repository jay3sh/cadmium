
import sys
sys.path.append('./src')
from cadmium import Revolution

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
