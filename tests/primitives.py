
import os
import sys
sys.path.append('../src')
from unittest import TestCase
import difflib

import cadmium

def generate_data():
  cyl = cadmium.Cylinder(r=5, h=10, center=True)
  cyl.toSTL('data/cylinder.stl')
  cyl.toJSON('data/cylinder.json.gz',compress=True)

  box = cadmium.Box(x=4,y=4,z=4, center=True)
  box.toSTL('data/box.stl')
  box.toJSON('data/box.json.gz', compress=True)

  cone = cadmium.Cone(r=5,h=10, center=True)
  cone.toSTL('data/cone.stl')
  cone.toJSON('data/cone.json.gz', compress=True)

  wedge = cadmium.Wedge(dx=5,dy=5,dz=5, center=True)
  wedge.toSTL('data/wedge.stl')
  wedge.toJSON('data/wedge.json.gz', compress=True)

  torus = cadmium.Torus(r1=1, r2=.2, center=True)
  torus.toSTL('data/torus.stl')
  torus.toJSON('data/torus.json.gz', compress=True)

  sph = cadmium.Sphere(r=1, center=True)
  sph.toSTL('data/sphere.stl')
  sph.toJSON('data/sphere.json.gz', compress=True)

def are_same(fn1, fn2):
  return difflib.SequenceMatcher(
    None, open(fn1).read(), open(fn2).read()).ratio() > 0.95

class CylinderTest(TestCase):
  def test(self):
    cyl = cadmium.Cylinder(r=5, h=10, center=True)
    cyl.toSTL('cylinder.stl')
    self.assertTrue(are_same('cylinder.stl','data/cylinder.stl'))
    os.remove('cylinder.stl')
    cyl.toJSON('cylinder.json.gz', compress=True)
    self.assertTrue(are_same('cylinder.json.gz','data/cylinder.json.gz'))
    os.remove('cylinder.json.gz')

class BoxTest(TestCase):
  def test(self):
    box = cadmium.Box(x=4,y=4,z=4, center=True)
    box.toSTL('box.stl')
    self.assertTrue(are_same('box.stl','data/box.stl'))
    os.remove('box.stl')
    box.toJSON('box.json.gz', compress=True)
    self.assertTrue(are_same('box.json.gz','data/box.json.gz'))
    os.remove('box.json.gz')

class ConeTest(TestCase):
  def test(self):
    cone = cadmium.Cone(r=5,h=10, center=True)
    cone.toSTL('cone.stl')
    self.assertTrue(are_same('cone.stl','data/cone.stl'))
    os.remove('cone.stl')
    cone.toJSON('cone.json.gz', compress=True)
    self.assertTrue(are_same('cone.json.gz','data/cone.json.gz'))
    os.remove('cone.json.gz')

class WedgeTest(TestCase):
  def test(self):
    wedge = cadmium.Wedge(dx=5,dy=5,dz=5, center=True)
    wedge.toSTL('wedge.stl')
    self.assertTrue(are_same('wedge.stl','data/wedge.stl'))
    os.remove('wedge.stl')
    wedge.toJSON('wedge.json.gz', compress=True)
    self.assertTrue(are_same('wedge.json.gz','data/wedge.json.gz'))
    os.remove('wedge.json.gz')

class TorusTest(TestCase):
  def test(self):
    torus = cadmium.Torus(r1=1, r2=.2, center=True)
    torus.toSTL('torus.stl')
    self.assertTrue(are_same('torus.stl', 'data/torus.stl'))
    os.remove('torus.stl')
    torus.toJSON('torus.json.gz', compress=True)
    self.assertTrue(are_same('torus.json.gz', 'data/torus.json.gz'))
    os.remove('torus.json.gz')

class SphereTest(TestCase):
  def test(self):
    sph = cadmium.Sphere(r=1, center=True)
    sph.toSTL('sphere.stl')
    self.assertTrue(are_same('sphere.stl','data/sphere.stl'))
    os.remove('sphere.stl')
    sph.toJSON('sphere.json.gz', compress=True)
    self.assertTrue(are_same('sphere.json.gz','data/sphere.json.gz'))
    os.remove('sphere.json.gz')

if __name__ == '__main__':
  generate_data()
