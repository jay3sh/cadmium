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

from cadmium.solid import Solid

def unique(seq):
  noDupes = [] 
  [noDupes.append(i) for i in seq if not noDupes.count(i)] 
  return noDupes

class Revolution(Solid):

  def __init__(self,
    knotVector=[], controlPoints=[], degree=3, center=False):

    uniqueKnots = unique(knotVector)
    frequency = [ knotVector.count(knot) for knot in uniqueKnots ]

    knots = TColStd_Array1OfReal(0, len(uniqueKnots)-1)
    for i in range(len(uniqueKnots)):
      knots.SetValue(i, uniqueKnots[i])

    mults = TColStd_Array1OfInteger(0, len(frequency)-1)
    for i in range(len(frequency)):
      mults.SetValue(i,frequency[i])

    poles = TColgp_Array1OfPnt(0, len(controlPoints)-1)
    for i in range(len(controlPoints)):
      p = controlPoints[i]
      poles.SetValue(i, gp_Pnt(p[0],p[1],p[2]))

    curve = Geom_BSplineCurve(poles, knots, mults, degree)
    h_curve = Handle_Geom_BSplineCurve(curve)

    X_axis = gp_Ax1(gp_Pnt(0,0,0),gp_Dir(1,0,0))
    
    self.instance = BRepPrimAPI_MakeRevolution(h_curve)
    Solid.__init__(self, self.instance.Shape(), center=center)

