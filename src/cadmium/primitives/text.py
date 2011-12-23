# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import os
import math
import urllib

import fontforge
from OCC.gp import gp_Pnt, gp_Vec
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.Geom import Geom_BezierCurve
from OCC.BRepBuilderAPI import \
  BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse

from cadmium.solid import Solid
import cadmium

INF = math.tan(math.pi/2) # infinity

class Glyph(Solid):
  xmax = -INF
  xmin = INF
  ymax = -INF
  ymin = INF
  zmax = -INF
  zmin = INF

  def __init__(self, char, thickness, font=None, fontpath=None, center=False):
    if font:
      self.font = font
    elif fontpath:
      self.font = fontforge.open(fontpath)

    self.char = char
    self.center = center
    glyph = self.font[str(char)]

    self.thickness = thickness
    self.bbox = glyph.boundingBox()
    self.left_side_bearing = glyph.left_side_bearing
    self.right_side_bearing = glyph.right_side_bearing

    if cadmium._brep_caching_enabled_:
      breppath = os.path.join(cadmium._brep_cache_path_,
        self.get_signature(char,self.font.path,thickness,center))
      if os.path.exists(breppath):
        Solid.__init__(self, None)
        self.fromBREP(breppath)
      else:
        Solid.__init__(self, self.char_to_solid(glyph), center=center)
        self.toBREP(breppath)

  def get_signature(self, *args, **kwds):
    signature = self.__class__.__name__
    for arg in args:
      if type(arg) == str:
        signature += urllib.quote_plus(arg)
      else:
        signature += str(arg)
    return signature

  def add_to_wire(self, points, wire):
    array=TColgp_Array1OfPnt(1, len(points))
    for i in range(len(points)):
      array.SetValue(i+1, points[i])
    curve = Geom_BezierCurve(array)
    me = BRepBuilderAPI_MakeEdge(curve.GetHandle())    
    wire.Add(me.Edge())

  def char_to_solid(self, glyph):

    layer = glyph.layers['Fore']
    bodies = []
    
    for contour in layer:
      i = 0
      total = len(contour)
      curve_points = []

      if total <= 2:
        # Can't make solid out of 1 or 2 points
        continue

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
      extrusion_vector = gp_Vec(0, 0, self.thickness)
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
        positive_union = None
        for body in bodies:
          if body['isClockwise'] == 1:
            if positive_union:
              positive_union = BRepAlgoAPI_Fuse(
                positive_union.Shape(), body['prism'].Shape())
            else:
              positive_union = body['prism']

        negative_union = None
        for body in bodies:
          if body['isClockwise'] == 0:
            if negative_union:
              negative_union = BRepAlgoAPI_Fuse(
                negative_union.Shape(), body['prism'].Shape())
            else:
              negative_union = body['prism']
        
        if positive_union and negative_union:
          final = BRepAlgoAPI_Cut(
            positive_union.Shape(), negative_union.Shape())
        elif positive_union:
          final = positive_union
        elif negative_union:
          final = negative_union
        return final.Shape()

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
  xmax = -INF
  xmin = INF
  ymax = -INF
  ymin = INF
  zmax = -INF
  zmin = INF

  def load_font(self, fontpath):
    if fontpath.find('/') >= 0 and cadmium._abs_fontpath_allowed_:
      return fontforge.open(fontpath)
    else:
      # Lookup in fonts directory
      if os.path.exists(cadmium._font_dir_):
        available_fonts = os.listdir(cadmium._font_dir_)
        if fontpath in available_fonts:
          return fontforge.open(os.path.join(cadmium._font_dir_, fontpath))
    raise Exception('Font not found')

  def __init__(self, text, fontpath, thickness=1,
    width=0, height=0, center=False):

    self.text = text

    self.font = self.load_font(fontpath)

    self.width = 0
    self.instance = None
    for char in text:
      c = None
      if char >= 'a' and char <= 'z':
        c = char
      elif char >= 'A' and char <= 'Z':
        c = char
      elif char == ' ':
        space = self.font['space']
        space_width = space.left_side_bearing + space.right_side_bearing
        self.width += space_width
        self.xmax += space_width
      else:
        c = self._char_map_.get(char)
      
      if not c: continue
        
      g = Glyph(c, thickness=1, font=self.font, center=True)
      g_xmin, g_ymin, g_zmin, g_xmax, g_ymax, g_zmax = g.getBoundingBox()
      g_xspan = g_xmax - g_xmin
      g_yspan = g_ymax - g_ymin
      g_zspan = g_zmax - g_zmin

      if self.instance:
        g.translate(x=(self.width+g.left_side_bearing+(g_xspan/2)))
        ymax_target = g.bbox[3]
        g.translate(y=(ymax_target-g_yspan/2))

        self.instance += g
        self.width += g.left_side_bearing+g_xspan+g.right_side_bearing
      else:
        ymax_target = g.bbox[3]
        g.translate(y=(ymax_target-g_yspan/2))
        self.instance = g
        self.width = (g_xspan/2)+g.right_side_bearing

    Solid.__init__(self, self.instance, center=center)

    xmin, ymin, zmin, xmax, ymax, zmax = self.getBoundingBox()
    if width and height:
      self.scale(scaleX = width*1.0/(xmax-xmin),
        scaleY = height*1.0/(ymax-ymin),
        scaleZ = thickness)
    elif (width and not height):
      self.scale(scaleX = width*1.0/(xmax-xmin),
        scaleY = width*1.0/(xmax-xmin),
        scaleZ = thickness)
    elif (height and not width):
      self.scale(scaleX = height*1.0/(ymax-ymin),
        scaleY = height*1.0/(ymax-ymin),
        scaleZ = thickness)

