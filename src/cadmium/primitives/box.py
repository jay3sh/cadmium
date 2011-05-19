
from cadmium.polyhedron import Polyhedron
from cadmium.primitives import Mesh

class Box(Polyhedron, Mesh):

  def __init__(self, x=10, y=10, z=10):
    Mesh.__init__(self)
    self._generate(x, y, z)
    Polyhedron.__init__(self)

  def _generate(self, x, y, z):
    v = [
      [-x/2, -y/2, -z/2],
      [ x/2, -y/2, -z/2],
      [ x/2,  y/2, -z/2],
      [-x/2,  y/2, -z/2],
      [-x/2, -y/2,  z/2],
      [ x/2, -y/2,  z/2],
      [ x/2,  y/2,  z/2],
      [-x/2,  y/2,  z/2] 
    ]
    
    for x in v: self.save_vertex(x)

    self.save_face([v[3], v[2], v[1]])
    self.save_face([v[3], v[1], v[0]])

    self.save_face([v[4], v[5], v[6]])
    self.save_face([v[4], v[6], v[7]])

    self.save_face([v[7], v[6], v[2]])
    self.save_face([v[7], v[2], v[3]])

    self.save_face([v[5], v[4], v[0]])
    self.save_face([v[5], v[0], v[1]])

    self.save_face([v[6], v[5], v[1]])
    self.save_face([v[6], v[1], v[2]])

    self.save_face([v[4], v[7], v[3]])
    self.save_face([v[4], v[3], v[0]])
