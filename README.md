Cadmium is a python library for Solid Modelling

Cadmium allows you to write python code to create primitive objects (Box, Cylinder, Sphere, etc.) and apply CSG operations (Addition, Subtraction, Intersection) on them to create advanced solid models. The primitives have support for affine transformations too (translation, rotation).

Screenshots 
-----------
[here](http://jayesh3.github.com/cadmium/).

Typical Solid modelling code with Cadmium
------------------------------------------
    from cadmium import *

    box = Box(x=4, y=4, z=4).rotate(Z_axis, 30)
    cyl = Cylinder(radius=2, height=4).translate(-1,0,0)

    solid = box + cyl

    solid.toSTL('solid.stl')

Getting Cadmium
---------------------------

    git clone https://github.com/jayesh3/cadmium.git cadmium
    cd cadmium
    python setup.py install

Getting Dependencies - PythonOCC
---------------------------------
Cadmium depends on PythonOCC which in turn requires OpenCASCADE.

The easiest way to setup PythonOCC and OpenCASCADE is to do it in Ubuntu server VM (unless you run Ubuntu natively). Although, PythonOCC includes some GUI utilities Cadmium doesn't need them, so you can use Ubuntu server VM.

To install OpenCASCADE just do `apt-get install libopencascade-dev`. You can get PythonOCC from [here](http://www.pythonocc.org/download/). If you choose to build it from source [these instructions](http://code.google.com/p/pythonocc/source/browse/trunk/INSTALL) are helpful.

Running example code
---------------------

    python examples/<python-script> <filename.stl>

Details
--------------------------
Cadmium is inspired by the [OpenSCAD project](http://www.openscad.org/), but it is a completely independent implementation. Here is what is different about Cadmium.

* Write your code in Python. No need to learn new syntax. Use your favorite python features as you do advanced calculations for solid modelling.
* Cadmium has no GUI. It only generates STL files (other formats may be supported in future). You can view these STL files in your favorite STL viewer, on your favorite OS. Becase Cadmium has no GUI, it's very light weight and has minimal dependencies. Hence it should be portable to any platform on which you can install PythonOCC
* All of the Cadmium code itself is written in Python, hence easy to maintain
* Cadmium is only creates easy-to-use abstraction on top of PythonOCC. All the real work is done by [PythonOCC](http://www.pythonocc.org/) and the underlying [OpenCASCADE library](http://www.opencascade.org/).

Cadmium is a work in progress. Bug reports and patches are welcome.

