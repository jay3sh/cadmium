#!/usr/bin/env python

from distutils.core import setup

setup(name='Cadmium',
      version='0.1',
      description='Solid modelling library',
      author='Jayesh Salvi',
      author_email='jayesh@3dtin.com',
      url='http://jayesh3.github.com/cadmium/',
      packages=['cadmium', 'cadmium.primitives'],
      package_dir={'cadmium':'src/cadmium', 
        'cadmium.primitives':'src/cadmium/primitives'},
     )
