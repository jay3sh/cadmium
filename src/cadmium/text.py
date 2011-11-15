# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import fontforge
from OCC.gp import gp_Pnt, gp_Vec
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.Geom import Geom_BezierCurve
from OCC.BRepBuilderAPI import \
  BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse

from cadmium.solid import Solid
import math
INF = math.tan(math.pi/2) # infinity

class Glyph(Solid):
  xmax = -INF
  xmin = INF
  ymax = -INF
  ymin = INF
  zmax = -INF
  zmin = INF
  def __init__(self, char, font, thickness):
    print self.xmax, self.xmin
    print self.ymax, self.ymin
    print self.zmax, self.zmin
    self.font = font
    self.thickness = thickness
    self.instance = self.char_to_solid(char)
    Solid.__init__(self, self.instance)

  def update_extents(self, point):
    self.xmax = max(self.xmax, point.X())
    self.xmin = min(self.xmin, point.X())
    self.ymax = max(self.ymax, point.Y())
    self.ymin = min(self.ymin, point.Y())
    self.zmax = max(self.zmax, point.Z())
    self.zmin = min(self.zmin, point.Z())

  def add_to_wire(self, points, wire):
    array=TColgp_Array1OfPnt(1, len(points))
    for i in range(len(points)):
      array.SetValue(i+1, points[i])
      self.update_extents(points[i])
    curve = Geom_BezierCurve(array)
    me = BRepBuilderAPI_MakeEdge(curve.GetHandle())    
    wire.Add(me.Edge())

  def char_to_solid(self, c):
    glyph = self.font[c]

    layer = glyph.layers['Fore']
    bodies = []
    
    for contour in layer:
      i = 0
      total = len(contour)
      curve_points = []

      wire = BRepBuilderAPI_MakeWire()
      for point in contour:
        if point.on_curve:
          if i > 0:
            # Complete old curve
            curve_points.append(gp_Pnt(point.x, point.y, 0))
            self.add_to_wire(curve_points, wire)

          if i < total:
            # Start new curve
            curve_points = [gp_Pnt(point.x, point.y, 0)]

          if i == total-1:
            first = contour[0]
            curve_points.append(gp_Pnt(first.x, first.y, 0))
            self.add_to_wire(curve_points, wire)
        else:
          curve_points.append(gp_Pnt(point.x, point.y, 0))
          if i == total-1:
            first = contour[0]
            curve_points.append(gp_Pnt(first.x, first.y, 0))
            self.add_to_wire(curve_points, wire)
        i += 1

      face = BRepBuilderAPI_MakeFace(wire.Wire())
      extrusion_vector = gp_Vec(0, 0, 100)
      prism = BRepPrimAPI_MakePrism(face.Shape(), extrusion_vector)

      bodies.append(dict(
        prism = prism,
        isClockwise = contour.isClockwise(),
      ))

    if len(bodies) > 0:
      if len(bodies) == 1:
        return bodies[0]['prism'].Shape()
      elif len(bodies) > 1:
        final = None
        for body in bodies:
          if not final:
            final = body
          else:
            if body['isClockwise'] and final['isClockwise']:
              union = BRepAlgoAPI_Fuse(
                body['prism'].Shape(), final['prism'].Shape())
              final = dict(
                prism = union,
                isClockwise = 1
              )
            elif not body['isClockwise'] and final['isClockwise']:
              sub = BRepAlgoAPI_Cut(
                final['prism'].Shape(), body['prism'].Shape())
              final = dict(
                prism = sub,
                isClockwise = 0
              )
            elif body['isClockwise'] and not final['isClockwise']:
              sub = BRepAlgoAPI_Cut(
                body['prism'].Shape(), final['prism'].Shape())
              final = dict(
                prism = sub,
                isClockwise = 0
              )
            elif not body['isClockwise'] and not final['isClockwise']:
              union = BRepAlgoAPI_Fuse(
                body['prism'].Shape(), final['prism'].Shape())
              final = dict(
                prism = union,
                isClockwise = 0
              )
        return final['prism'].Shape()
class Text(Solid):
  _char_map_ = {
    '!' : 'exclam',
    '"' : 'quotedbl',
    '#' : 'numbersign',
    '$' : 'dollar',
    '%' : 'percent',
    '&' : 'ampersand',
    '\'': 'quotesingle',
    '(' : 'parenleft',
    ')' : 'parenright',
    '*' : 'asterisk',
    '+' : 'plus',
    ',' : 'comma',
    '-' : 'hyphen',
    '.' : 'period',
    '/' : 'slash',
    '0' : 'zero',
    '1' : 'one',
    '2' : 'two',
    '3' : 'three',
    '4' : 'four',
    '5' : 'five',
    '6' : 'six',
    '7' : 'seven',
    '8' : 'eight',
    '9' : 'nine',
    ':' : 'colon',
    ';' : 'semicolon',
    '<' : 'less',
    '=' : 'equal',
    '>' : 'greater',
    '?' : 'question',
    '@' : 'at',
    '[' : 'bracketleft',
    '\\': 'backslash',
    ']' : 'bracketright',
    '^' : 'asciicircum',
    '_' : 'underscore',
    '`' : 'grave',
    '{' : 'braceleft',
    '|' : 'bar',
    '}' : 'braceright',
    '~' : 'asciitilde'
  }

  def __init__(self, text, fontpath, thickness=1):

    font = fontforge.open(fontpath)

    self.instance = None
    for char in text:
      if char > 'a' and char < 'z':
        c = char
      elif char > 'A' and char < 'Z':
        c = char
      else:
        c = self._char_map_.get(char)
      
      if not c: continue
        
      if self.instance:
        #self.instance = BRepAlgoAPI_Fuse(
        #  self.instance.Shape(), self.char_to_solid(c))
        self.instance += Glyph(c, font, thickness)
      else:
        self.instance = Glyph(c, font, thickness)
        #self.instance = self.char_to_solid(c)

    Solid.__init__(self, self.instance)
  
