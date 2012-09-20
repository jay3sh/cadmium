# 
# Cadmium - Python library for Solid Modelling
# Copyright (C) 2011 Jayesh Salvi [jayesh <at> 3dtin <dot> com]
#


from OCC.gp import *
from OCC.TColgp import TColgp_Array1OfPnt
from OCC.TColStd import TColStd_Array1OfReal,TColStd_Array1OfInteger
from OCC.Geom import Geom_BezierCurve,Geom_BSplineCurve,Handle_Geom_BSplineCurve
from OCC.BRepPrimAPI import *
from OCC.GeomAPI import GeomAPI_PointsToBSpline
from OCC.Geom import Geom_SurfaceOfRevolution
from OCC.BRepBuilderAPI import \
  BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace

from cadmium.solid import Solid

class Extrusion(Solid):

  def __init__(self,center=False):
    self.thickness = 10
    knots = TColStd_Array1OfReal(0, 5)
    knots.SetValue(0,0)
    knots.SetValue(1,1)
    knots.SetValue(2,5)
    knots.SetValue(3,6)
    knots.SetValue(4,8)
    knots.SetValue(5,9)

    mults = TColStd_Array1OfInteger(0, 5)
    mults.SetValue(0,4)
    mults.SetValue(1,1)
    mults.SetValue(2,1)
    mults.SetValue(3,1)
    mults.SetValue(4,1)
    mults.SetValue(5,4)

    poles = TColgp_Array1OfPnt(0, 7)
    poles.SetValue(0, gp_Pnt(0, 1, 0))
    poles.SetValue(1, gp_Pnt(0, 1, 0))
    poles.SetValue(2, gp_Pnt(0, 2, 1))
    poles.SetValue(3, gp_Pnt(0, 3, 2))
    poles.SetValue(4, gp_Pnt(0, 4, 2.5))
    poles.SetValue(5, gp_Pnt(0, 1, 3))
    poles.SetValue(6, gp_Pnt(0, 0.5, 4))
    poles.SetValue(7, gp_Pnt(0, 1, 0))

    curve = Geom_BSplineCurve(poles, knots, mults, 3)
    me = BRepBuilderAPI_MakeEdge(curve.GetHandle())    

    wire = BRepBuilderAPI_MakeWire()
    wire.Add(me.Edge())

    face = BRepBuilderAPI_MakeFace(wire.Wire())
    extrusion_vector = gp_Vec(self.thickness,0,0)
    self.instance = BRepPrimAPI_MakePrism(face.Shape(), extrusion_vector)
    Solid.__init__(self, self.instance.Shape(), center=center)


