# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math

from cadmium.polyhedron import Polyhedron
from cadmium.primitives import Mesh

def sph2cartesian(r, theta, phi):
  return [
    r * math.sin(theta) * math.sin(phi),
    r * math.cos(theta),
    r * math.sin(theta) * math.cos(phi)
  ]

class Sphere(Polyhedron, Mesh):

  DIV = 32

  def __init__(self, radius=10):
    Mesh.__init__(self)
    self._generate(radius)
    Polyhedron.__init__(self)

  def _generate(self, r):
    dtheta = 2*math.pi/self.DIV
    dphi = 2*math.pi/self.DIV

    for i in range(self.DIV):
      curphi = i * dphi
      if i-1 < 0:
        lastphi = (self.DIV - 1) * dphi
      else:
        lastphi = (i-1) * dphi

      for j in range(self.DIV/2):
        curtheta = j * dtheta
        nexttheta = (j+1) * dtheta

        if j == 0:
          v1 = sph2cartesian(r, curtheta, lastphi)   
          v2 = sph2cartesian(r, nexttheta, curphi)   
          v3 = sph2cartesian(r, nexttheta, lastphi)   
          self.save_vertex(v1)
          self.save_vertex(v2)
          self.save_vertex(v3)
          self.save_face([v1,v3,v2])
        elif j == self.DIV-1:
          v0 = sph2cartesian(r, curtheta, curphi)   
          v1 = sph2cartesian(r, curtheta, lastphi)   
          v2 = sph2cartesian(r, nexttheta, curphi)   
          self.save_vertex(v0)
          self.save_vertex(v1)
          self.save_vertex(v2)
          self.save_face([v0,v1,v2])
        else:
          v0 = sph2cartesian(r, curtheta, curphi)   
          v1 = sph2cartesian(r, curtheta, lastphi)   
          v2 = sph2cartesian(r, nexttheta, curphi)   
          v3 = sph2cartesian(r, nexttheta, lastphi)   
          self.save_vertex(v0)
          self.save_vertex(v1)
          self.save_vertex(v2)
          self.save_vertex(v3)
          self.save_face([v0,v1,v2])
          self.save_face([v1,v3,v2])

