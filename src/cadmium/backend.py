
from ctypes import *

libc = cdll.LoadLibrary('/lib/libc.so.6')
libcsg = cdll.LoadLibrary('build/libcsgop.so')

csgop = libcsg.csgop
memfree = libc.free
ERR_NOT_SIMPLE = libcsg.ERR_NOT_SIMPLE
OP_UNION = libcsg.OP_UNION
OP_INTERSECTION = libcsg.OP_INTERSECTION
OP_SUBTRACTION = libcsg.OP_SUBTRACTION

PDOUBLE = POINTER(c_double)
PPDOUBLE = POINTER(PDOUBLE)
PINT = POINTER(c_int)
PPINT = POINTER(PINT)
DBLARR = c_double * 3
INTARR = c_int * 3

# Function prototype
csgop.argtypes = [ 
  PPDOUBLE, c_int, c_int, PPINT, c_int, c_int,
  PPDOUBLE, c_int, c_int, PPINT, c_int, c_int, c_int ]

# Function return data type
PPDOUBLE = POINTER(POINTER(c_double))
PPINT = POINTER(POINTER(c_int))

class PolyPack(Structure):
  _fields_ = [
              ('error', c_int),
              ('num_vertices', c_int),
              ('num_faces', c_int),
              ('vertices', PPDOUBLE),
              ('faces', PPINT),
              ]

csgop.restype = POINTER(PolyPack)
