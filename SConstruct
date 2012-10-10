
env = Environment(SHLIBPREFIX='')
env.SharedLibrary('src/cadmium/occ',['src/cadmium/occ.cpp'],
  CPPFLAGS='-pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall '+\
    '-Wstrict-prototypes -fPIC -I/usr/include/python2.7 '+\
    '-I/home/jayesh/occ-usr/inc',
  LIBS=['TKernel','PTKernel','TKMath','TKService','TKV3d','TKV2d',
    'TKBRep','TKIGES','TKSTL','TKSTEP','TKSTEPAttr','TKSTEP209',
    'TKSTEPBase','TKShapeSchema','TKGeomBase','TKGeomAlgo','TKG3d','TKG2d',
    'TKXSBase','TKPShape','TKShHealing','TKHLR','TKTopAlgo','TKMesh','TKPrim',
    'TKCDF','TKBool','TKBO','TKFillet','TKOffset'
  ],
  LINKFLAGS=\
    '-pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,'+\
    '-Bsymbolic-functions '+\
    '-Xlinker -rpath -Xlinker /home/jayesh/occ-usr/lib',
  LIBPATH=['/home/jayesh/occ-usr/lib'])
