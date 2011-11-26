
from OCC.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.BRepBuilderAPI import BRepBuilderAPI_GTransform
from OCC.gp import gp_GTrsf, gp_Trsf
from OCC.Precision import Precision_Angular, Precision_Confusion
from OCC import StlAPI

shape = BRepPrimAPI_MakeCylinder(20,40).Shape()

xform = gp_Trsf()
xform.SetValues(
  1.5, 0, 0, 0,
  0, 1, 0, 0,
  0, 0, 1, 0,
  Precision_Angular(), Precision_Confusion()
);
brep = BRepBuilderAPI_GTransform(shape, gp_GTrsf(xform), False)
brep.Build()
shape = brep.Shape()


stl_writer = StlAPI.StlAPI_Writer()
stl_writer.Write(shape, 'scaled-cylinder.stl')
