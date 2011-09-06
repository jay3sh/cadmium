'''
Python library for Solid Modelling
'''

from OCC.gp import *
X_axis = gp_Ax1(gp_Pnt(0,0,0),gp_Dir(1,0,0))
Y_axis = gp_Ax1(gp_Pnt(0,0,0),gp_Dir(0,1,0))
Z_axis = gp_Ax1(gp_Pnt(0,0,0),gp_Dir(0,0,1))

import solid 
import primitives.cylinder
import primitives.sphere
import primitives.box
import primitives.cone
import primitives.wedge
import primitives.torus

Cylinder = primitives.cylinder.Cylinder
Sphere = primitives.sphere.Sphere
Box = primitives.box.Box
Cone = primitives.cone.Cone
Wedge = primitives.wedge.Wedge
Torus = primitives.torus.Torus

Solid = solid.Solid

# Value range constants
POSITIVE = 1
NEGATIVE = 2

# Alignment constants
A_MIN = 1
A_MAX = 2
A_CENTER = 3


#
# Annotation decorators
#
def description(*arg, **kwdArg):
  def decorator(func):
    return func
  return decorator

def param(*arg, **kwdArg):
  def decorator(func):
    return func
  return decorator

class CadmiumException(BaseException):
  '''
  Useful mainly for validating user provided input for Solid instantiations
  '''
  def __init__(self, msg):
    self.msg = msg
    BaseException.__init__(self, msg)
