# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

import math

class Matrix():
  def __init__(self, r=None):
    if r:
      self.r = r
    else:
      self.r = [ 1, 0, 0, 0,
                 0, 1, 0, 0,
                 0, 0, 1, 0,
                 0, 0, 0, 1 ]

  def mulV3(self, v):
    r = self.r
    return [
      r[0] * v[0] + r[4] * v[1] + r[8] * v[2] + r[12],
      r[1] * v[0] + r[5] * v[1] + r[9] * v[2] + r[13],
      r[2] * v[0] + r[6] * v[1] + r[10] * v[2] + r[14],
      r[3] * v[0] + r[7] * v[1] + r[11] * v[2] + r[15]
    ];

  def __mul__(self, other):
    a = self.r
    b = other.r
    r = list(range(16))
    r[0] = b[0] * a[0] + b[0+1] * a[4] + b[0+2] * a[8] + b[0+3] * a[12]
    r[0+1] = b[0] * a[1] + b[0+1] * a[5] + b[0+2] * a[9] + b[0+3] * a[13]
    r[0+2] = b[0] * a[2] + b[0+1] * a[6] + b[0+2] * a[10] + b[0+3] * a[14]
    r[0+3] = b[0] * a[3] + b[0+1] * a[7] + b[0+2] * a[11] + b[0+3] * a[15]
    r[4] = b[4] * a[0] + b[4+1] * a[4] + b[4+2] * a[8] + b[4+3] * a[12]
    r[4+1] = b[4] * a[1] + b[4+1] * a[5] + b[4+2] * a[9] + b[4+3] * a[13]
    r[4+2] = b[4] * a[2] + b[4+1] * a[6] + b[4+2] * a[10] + b[4+3] * a[14]
    r[4+3] = b[4] * a[3] + b[4+1] * a[7] + b[4+2] * a[11] + b[4+3] * a[15]
    r[8] = b[8] * a[0] + b[8+1] * a[4] + b[8+2] * a[8] + b[8+3] * a[12]
    r[8+1] = b[8] * a[1] + b[8+1] * a[5] + b[8+2] * a[9] + b[8+3] * a[13]
    r[8+2] = b[8] * a[2] + b[8+1] * a[6] + b[8+2] * a[10] + b[8+3] * a[14]
    r[8+3] = b[8] * a[3] + b[8+1] * a[7] + b[8+2] * a[11] + b[8+3] * a[15]
    r[12] = b[12] * a[0] + b[12+1] * a[4] + b[12+2] * a[8] + b[12+3] * a[12]
    r[12+1] = b[12] * a[1] + b[12+1] * a[5] + b[12+2] * a[9] + b[12+3] * a[13]
    r[12+2] = b[12] * a[2] + b[12+1] * a[6] + b[12+2] * a[10] + b[12+3] * a[14]
    r[12+3] = b[12] * a[3] + b[12+1] * a[7] + b[12+2] * a[11] + b[12+3] * a[15]
    return Matrix(r);

class Quat():
  def __init__(self, axis, angle):
    self.w = math.cos(angle/2.0);
    sin = math.sin(angle/2.0);
    self.x = axis[0] * sin;
    self.y = axis[1] * sin;
    self.z = axis[2] * sin;

  def toM4(self):
    return Matrix([
      1.0 - 2.0 * ( self.y * self.y + self.z * self.z ),
      2.0 * (self.x * self.y + self.z * self.w),
      2.0 * (self.x * self.z - self.y * self.w),
      0.0,
      2.0 * ( self.x * self.y - self.z * self.w ),
      1.0 - 2.0 * ( self.x * self.x + self.z * self.z ),
      2.0 * (self.z * self.y + self.x * self.w ),
      0.0,
      2.0 * ( self.x * self.z + self.y * self.w ),
      2.0 * ( self.y * self.z - self.x * self.w ),
      1.0 - 2.0 * ( self.x * self.x + self.y * self.y ),
      0.0,
      0,
      0,
      0,
      1.0 
    ])

