# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

#!/usr/bin/python

import os
import sys
import json

from cadmium.backend import *

class Polyhedron():

  def __init__(self, ppack=None):
    if ppack:
      self.__unpack_c_data__(ppack)

    self.c_vertices = None
    self.c_faces = None

  def __unpack_c_data__(self, ppack):
    pack = ppack[0]

    if pack.error == ERR_NOT_SIMPLE:
      raise Exception('NOT_SIMPLE')

    self.vertices = []
    self.faces = []
    for i in range(pack.num_vertices):
      x = pack.vertices[i]
      self.vertices.append([x[0], x[1], x[2]])

    for i in range(pack.num_faces):
      x = pack.faces[i]
      self.faces.append([x[0], x[1], x[2]])

    free_ppack(pack)

  def __make_c_data__(self):
    PDBLARR = PDOUBLE * len(self.vertices)
    PINTARR = PINT * len(self.faces)

    self.c_vertices = PDBLARR()

    for r in range(len(self.vertices)):
      self.c_vertices[r] = DBLARR()
      for c in range(len(self.vertices[r])):
        self.c_vertices[r][c] = self.vertices[r][c]

    self.c_faces = PINTARR()
    for r in range(len(self.faces)):
      self.c_faces[r] = INTARR()
      for c in range(len(self.faces[r])):
        self.c_faces[r][c] = self.faces[r][c]

  def get_c_data(self):
    if not self.c_vertices or not self.c_faces:
      self.__make_c_data__()
    return (self.c_vertices, len(self.vertices), self.c_faces, len(self.faces))

  def __add__(self, other):
    c_vertices_1, numvertices_1, c_faces_1, numfaces_1 = self.get_c_data()
    c_vertices_2, numvertices_2, c_faces_2, numfaces_2 = other.get_c_data()
    ppack = csgop(
      c_vertices_1, numvertices_1, 3, c_faces_1, numfaces_1, 3,
      c_vertices_2, numvertices_2, 3, c_faces_2, numfaces_2, 3, 
      1)
    return Polyhedron(ppack=ppack)

  def __mul__(self, other):
    c_vertices_1, numvertices_1, c_faces_1, numfaces_1 = self.get_c_data()
    c_vertices_2, numvertices_2, c_faces_2, numfaces_2 = other.get_c_data()
    ppack = csgop(
      c_vertices_1, numvertices_1, 3, c_faces_1, numfaces_1, 3,
      c_vertices_2, numvertices_2, 3, c_faces_2, numfaces_2, 3, 
      2)
    return Polyhedron(ppack=ppack)

  def __sub__(self, other):
    c_vertices_1, numvertices_1, c_faces_1, numfaces_1 = self.get_c_data()
    c_vertices_2, numvertices_2, c_faces_2, numfaces_2 = other.get_c_data()
    ppack = csgop(
      c_vertices_1, numvertices_1, 3, c_faces_1, numfaces_1, 3,
      c_vertices_2, numvertices_2, 3, c_faces_2, numfaces_2, 3, 
      3)
    return Polyhedron(ppack=ppack)

  def __str__(self):
    return json.dumps({
        'vertices' : self.vertices,
        'faces' : self.faces })

  def toSTL(self):

    import struct
    def sub(a, b):
      return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
    def cross(a, b):
      return [ a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0] ]

    triangles = []

    for f in self.faces:
      v = map(lambda x: self.vertices[x], f)
      normal = cross(sub(v[1], v[0]), sub(v[2], v[1])) 
      triangles.append(
        [ normal[0], normal[1], normal[2],
          v[0][0], v[0][1], v[0][2],
          v[1][0], v[1][1], v[1][2],
          v[2][0], v[2][1], v[2][2] ])

    tr_format = struct.Struct('<12f')
    attr_byte_count = struct.pack('H', 0)
    stl_header = 'Exported from Cadmium'+59*' '
    stlbin = struct.pack('80s', stl_header)
    stlbin += struct.pack('I', len(self.faces))
    for t in triangles:
      stlbin += tr_format.pack(
                  t[0], t[1], t[2],   # normal
                  t[3], t[4], t[5],   # vertex 1
                  t[6], t[7], t[8],   # vertex 2
                  t[9], t[10], t[11]) # vertex 3
      stlbin += attr_byte_count
    return stlbin

  def toOff(self):
    offout = 'OFF\n'
    offout += '%d %d 0\n'%(len(self.vertices), len(self.faces))
    for vertex in self.vertices:
      offout += ' '.join(map(str,vertex))+'\n'
    for face in self.faces:
      offout += str(len(face))+' '+' '.join(map(str,face))+'\n'
    return offout

  def fromOff(self, off):
    import re
    whitespace = re.compile('\s+')
    linecount = 0
    vcount = 0
    self.vertices = []
    self.faces = []
    for line in off.split('\n'):
      if line and len(line.strip()) > 0:
        if linecount == 1:
          numv, numf, nume = map(int, whitespace.split(line))

        if linecount > 1:
          if vcount < numv:
            self.vertices.append(map(float, whitespace.split(line)))
            vcount += 1
          else:
            self.faces.append(map(int, whitespace.split(line))[1:])

      linecount += 1

class PolyhedronSimple():
  def __init__(self, offname=None):
    if offname:
      off = open(offname, 'r').read()
      self.fromOff(off)
      os.remove(offname)

  def __add__(self, other):
    id = csgop_simple(self.toOff(), other.toOff(), 1)
    return Polyhedron(offname='%d.off'%(id))

  def __mul__(self, other):
    id = csgop_simple(self.toOff(), other.toOff(), 2)
    return Polyhedron(offname='%d.off'%(id))

  def __sub__(self, other):
    id = csgop_simple(self.toOff(), other.toOff(), 3)
    return Polyhedron(offname='%d.off'%(id))

  def toSTL(self):
    import struct
    def sub(a, b):
      return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
    def cross(a, b):
      return [ a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0] ]

    triangles = []

    for f in self.faces:
      v = map(lambda x: self.vertices[x], f)
      normal = cross(sub(v[1], v[0]), sub(v[2], v[1])) 
      triangles.append(
        [ normal[0], normal[1], normal[2],
          v[0][0], v[0][1], v[0][2],
          v[1][0], v[1][1], v[1][2],
          v[2][0], v[2][1], v[2][2] ])

    tr_format = struct.Struct('<12f')
    attr_byte_count = struct.pack('H', 0)
    stl_header = 'Exported from Cadmium'+59*' '
    stlbin = struct.pack('80s', stl_header)
    stlbin += struct.pack('I', len(self.faces))
    for t in triangles:
      stlbin += tr_format.pack(
                  t[0], t[1], t[2],   # normal
                  t[3], t[4], t[5],   # vertex 1
                  t[6], t[7], t[8],   # vertex 2
                  t[9], t[10], t[11]) # vertex 3
      stlbin += attr_byte_count
    return stlbin

  def toOff(self):
    offout = 'OFF\n'
    offout += '%d %d 0\n'%(len(self.vertices), len(self.faces))
    for vertex in self.vertices:
      offout += ' '.join(map(str,vertex))+'\n'
    for face in self.faces:
      offout += str(len(face))+' '+' '.join(map(str,face))+'\n'
    return offout

  def fromOff(self, off):
    import re
    whitespace = re.compile('\s+')
    linecount = 0
    vcount = 0
    self.vertices = []
    self.faces = []
    for line in off.split('\n'):
      if line and len(line.strip()) > 0:
        if linecount == 1:
          numv, numf, nume = map(int, whitespace.split(line))

        if linecount > 1:
          if vcount < numv:
            self.vertices.append(map(float, whitespace.split(line)))
            vcount += 1
          else:
            self.faces.append(map(int, whitespace.split(line))[1:])

      linecount += 1
