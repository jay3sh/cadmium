
import math

from cadmium.polyhedron import Polyhedron
from cadmium.primitives import Mesh

class Cylinder(Polyhedron, Mesh):

  DIV = 32

  def __init__(self, radius=2, height=4):
    Mesh.__init__(self)
    self._generate(radius, height)
    Polyhedron.__init__(self)

  def make_circle(self, r, h):
    center = [0.0, h/2, 0.0]
    self.save_vertex(center)

    for i in range(self.DIV):
      self.save_vertex([ 
        r*math.cos(2*math.pi * (1.0*i/self.DIV)),
        h/2,
        r*math.sin(2*math.pi * (1.0*i/self.DIV))
      ])

    for i in range(self.DIV):
      cur = i
      if i-1 < 0:
        last = self.DIV-1
      else:
        last = i-1
      curpoint = [ r * math.cos(2*math.pi * (1.0*cur/self.DIV)), 
                    h/2,
                    r * math.sin(2*math.pi * (1.0*cur/self.DIV)) ]
      lastpoint = [ r * math.cos(2*math.pi * (1.0*last/self.DIV)), 
                    h/2,
                    r * math.sin(2*math.pi * (1.0*last/self.DIV)) ]
      if h > 0:
        self.save_face([center, curpoint, lastpoint])
      else:
        self.save_face([center, lastpoint, curpoint])

  def _generate(self, r, h):
    self.make_circle(r, h) 
    self.make_circle(r, -h) 

    for i in range(self.DIV):
      cur = i
      if i-1 < 0:
        last  = self.DIV-1
      else:
        last = i-1

      v0 = [
          r * math.cos(2*math.pi * (1.0*cur/self.DIV)),
          h/2,
          r * math.sin(2*math.pi * (1.0*cur/self.DIV))];
      v1 = [
          r * math.cos(2*math.pi * (1.0*last/self.DIV)),
          h/2,
          r * math.sin(2*math.pi * (1.0*last/self.DIV))];
      v2 = [
          r * math.cos(2*math.pi * (1.0*cur/self.DIV)),
          -h/2,
          r * math.sin(2*math.pi * (1.0*cur/self.DIV))];
      v3 = [
          r * math.cos(2*math.pi * (1.0*last/self.DIV)),
          -h/2,
          r * math.sin(2*math.pi * (1.0*last/self.DIV))];

      self.save_face([v0, v2, v1]);
      self.save_face([v1, v2, v3]);
