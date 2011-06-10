# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#

from OCC.gp import *
X_axis = gp_Ax1(gp_Pnt(0,0,0),gp_Dir(1,0,0))
Y_axis = gp_Ax1(gp_Pnt(0,0,0),gp_Dir(0,1,0))
Z_axis = gp_Ax1(gp_Pnt(0,0,0),gp_Dir(0,0,1))

import polyhedronOCC
import primitives.cylinderOCC
import primitives.sphereOCC
import primitives.boxOCC
import primitives.coneOCC
import primitives.wedgeOCC
import primitives.torusOCC

Cylinder = primitives.cylinderOCC.Cylinder
Sphere = primitives.sphereOCC.Sphere
Box = primitives.boxOCC.Box
Cone = primitives.coneOCC.Cone
Wedge = primitives.wedgeOCC.Wedge
Torus = primitives.torusOCC.Torus

