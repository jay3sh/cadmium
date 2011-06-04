
import sys
sys.path.append('../src')
from cadmium.polyhedron import Polyhedron

offname = sys.argv[1]
stlname = sys.argv[2]

p = Polyhedron()
p.fromOff(open(offname, 'r').read())
stl = p.toSTL()

open(stlname, 'w').write(stl)

