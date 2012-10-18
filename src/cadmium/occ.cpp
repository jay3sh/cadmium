
#include <Python.h>
#include "structmember.h"

#define HAVE_LIMITS_H 1
#define HAVE_IOSTREAM 1
#define HAVE_IOMANIP 1

#include <iostream>
#include <sys/time.h>
#include <math.h>

#include <BRepTools.hxx>
#include <BRepBndLib.hxx>
#include <BRep_Builder.hxx>
#include <BRepPrimAPI_MakeBox.hxx>
#include <BRepPrimAPI_MakeTorus.hxx>
#include <BRepPrimAPI_MakeSphere.hxx>
#include <BRepPrimAPI_MakeCylinder.hxx>
#include <BRepPrimAPI_MakeCone.hxx>

#include <BRepAlgoAPI_Fuse.hxx>
#include <BRepAlgoAPI_Cut.hxx>

#include <BRepBuilderAPI_Transform.hxx>

#include <StlAPI_Writer.hxx>

typedef struct {
  PyObject_HEAD
  TopoDS_Shape shape;
} Shape;

static void
Shape_dealloc(Shape *self) {
  self->ob_type->tp_free((PyObject *)self);
}

static PyObject *
Shape_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {

  Shape *self;
  self = (Shape *)type->tp_alloc(type, 0);
  return (PyObject *)self;
}

static int
Shape_init(Shape *self, PyObject *args, PyObject *kwds) {
  return 0;
}

// 
// Affine transform methods
//
static PyObject*
Shape_translate(Shape *self, PyObject *args, PyObject *kwds)
{
  double dx=0.0, dy=0.0, dz=0.0;

  if (!PyArg_ParseTuple(args,"ddd", &dx, &dy, &dz)) {
    std::cout << "Failed to parse init args" << std::endl;
    return 0;
  }

  /*
  gp_Trsf trsf;
  gp_Vec delta(dx, dy, dz);
  trsf.SetTranslation(delta);
  BRepBuilderAPI_Transform brep(*(self->shape), trsf, Standard_False);
  brep.Build();
  self->shape = brep.Shape();
  */

  Py_INCREF(Py_None);
  return Py_None;
}

static PyMemberDef Shape_members[] = {
  { NULL }
};

static PyMethodDef Shape_methods[] = {
  { "translate", (PyCFunction) Shape_translate, METH_VARARGS, "Translate" },
  { NULL }
};

static PyTypeObject ShapeType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "occ.Shape",             /*tp_name*/
    sizeof(Shape), /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    0,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "Shape",                 /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    Shape_methods,           /* tp_methods */
    Shape_members,           /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Shape_init,      /* tp_init */
    0,                         /* tp_alloc */
    Shape_new,                 /* tp_new */
};

/******************************
 * Primitive creation methods
 ******************************/

static PyObject *
occ_makecon(PyObject *self, PyObject *args)
{
  /*
  double radius1;
  double radius2;
  double height;
  double pie;

  if (!PyArg_ParseTuple(args, "dddd", &radius1, &radius2, &height, &pie)) {
    std::cout << "Failed to parse args" << std::endl;
    return 0;
  }

  PyObject *pyShape = _PyObject_New(&ShapeType);
  PyObject_Init(pyShape, &ShapeType);

  ((Shape *)pyShape)->shape = (TopoDS_Shape *)
    &BRepPrimAPI_MakeCone(radius1, radius2, height, pie).Shape();

  Py_INCREF(pyShape);
  return pyShape;
  */
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *
occ_makebox(PyObject *self, PyObject *args)
{
  double x;
  double y;
  double z;

  if (!PyArg_ParseTuple(args, "ddd", &x, &y, &z)) {
    std::cout << "Failed to parse args" << std::endl;
    return 0;
  }

  PyObject *pyShape = _PyObject_New(&ShapeType);
  PyObject_Init(pyShape, &ShapeType);

  ((Shape *)pyShape)->shape = BRepPrimAPI_MakeBox(x, y, z).Shape();

  Py_INCREF(pyShape);
  return pyShape;
}

static PyObject *
occ_makesph(PyObject *self, PyObject *args)
{
  /*
  double radius;
  double phi;

  if (!PyArg_ParseTuple(args, "dd", &radius, &phi)) {
    std::cout << "Failed to parse args" << std::endl;
    return 0;
  }

  PyObject *pyShape = _PyObject_New(&ShapeType);
  PyObject_Init(pyShape, &ShapeType);

  ((Shape *)pyShape)->shape = 
    (TopoDS_Shape *)&BRepPrimAPI_MakeSphere(radius, phi).Shape();

  Py_INCREF(pyShape);
  return pyShape;
  */
  Py_INCREF(Py_None);
  return Py_None;
}

/*****************************
 * occ Module
 *****************************/

static PyMethodDef occ_methods[] = {
  { "makecon"   , occ_makecon   , METH_VARARGS , NULL } ,
  { "makebox"   , occ_makebox   , METH_VARARGS , NULL } ,
  { "makesph"   , occ_makesph   , METH_VARARGS , NULL } ,
  { NULL }  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initocc(void) 
{
  PyObject* m;

  if (PyType_Ready(&ShapeType) < 0)
      return;

  m = Py_InitModule3("occ", occ_methods, "OpenCASCADE wrapper module");

  Py_INCREF(&ShapeType);
  PyModule_AddObject(m, "Shape", (PyObject *)&ShapeType);

}
