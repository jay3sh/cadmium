# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

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

Cylinder = primitives.cylinder.Cylinder
Sphere = primitives.sphere.Sphere
Box = primitives.box.Box
Cone = primitives.cone.Cone
Wedge = primitives.wedge.Wedge

Solid = solid.Solid
