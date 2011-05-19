
`Cadmium` is a python library for Solid Modelling

Building and Installing Dependency - CGAL
-----------------------------------------

The only dependency for `Cadmium` is `CGAL`
Download [CGAL-3.8](https://gforge.inria.fr/frs/?group_id=52)

    unzip CGAL-3.8.zip
    cd CGAL-3.8
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Debug .
    make
    sudo make install

Building `Cadmium` backend
--------------------------
You need to have `SCons` install for this step

    cd cadmium
    scons

If you don't have Scons

    g++ -o src/cgal-wrapper/csgop.os -c -fPIC -I/usr/local/include src/cgal-wrapper/csgop.cpp
    g++ -o build/libcsgop.so -shared src/cgal-wrapper/csgop.os -L/usr/local/lib -lCGAL

