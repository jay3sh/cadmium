
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
  TopoDS_Shape *pShape;
} Shape;

static void
Shape_dealloc(Shape *self) {
  if(self->pShape) {
    delete self->pShape;
  }
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

static PyMemberDef Shape_members[] = {
  { NULL }
};

static PyMethodDef Shape_methods[] = {
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
occ_makecyl(PyObject *self, PyObject *args)
{
}

static PyObject *
occ_makebox(PyObject *self, PyObject *args)
{
}

/*****************************
 * occ Module
 *****************************/

static PyMethodDef occ_methods[] = {
  { "makecyl"   , occ_makecyl   , METH_VARARGS , NULL } ,
  { "makebox"   , occ_makebox   , METH_VARARGS , NULL } ,
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
