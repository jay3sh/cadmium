
from matrix import Matrix, Quat

class Mesh():
  def __init__(self):
    self.vertices = []
    self.vmap = {}
    self.faces = []

  def vtxkey(self, vertex):
    return '_'.join(map(str, vertex))

  def save_vertex(self, vertex):
    self.vmap[self.vtxkey(vertex)] = len(self.vertices)
    self.vertices.append(vertex)

  def save_face(self, face):
    self.faces.append(map(lambda x: self.vmap[self.vtxkey(x)], face))

  def translate(self, d):
    self.vertices = map(lambda v: map(lambda a: a[0]+a[1], zip(v, d)), self.vertices)

  def rotate(self, axis, angle):
    transform = Quat(axis, angle).toM4() * Matrix()
    self.vertices = map(lambda v: transform.mulV3(v), self.vertices)
