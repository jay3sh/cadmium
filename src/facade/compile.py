
import re
import os
import json
import inspect
import cadmium

def main():
  module_names = filter(
    lambda x: x != 'cadmium.py' and x != 'compile.py' and x.endswith('.py'),
    os.listdir('.'))
  module_names = map(lambda x: x.split('.')[0], module_names)

  std_classes = [ c[0] for c in inspect.getmembers(cadmium, inspect.isclass) ]

  expressions = {}

  for module_name in module_names:
    mod = __import__(module_name)
    classes = filter(lambda x: x[0] not in std_classes,
      inspect.getmembers(mod, inspect.isclass))

    assert len(classes) == 1
    usolid = classes[0][1]()
    meta = cadmium.inspectionData
    paramData = meta['paramData']
    argspec = inspect.getargspec(classes[0][1].__init__)
    argdetails = []
    i = 0
    for argname in argspec.args:
      if argname == 'self': continue
      argdetail = dict(
        name = argname,
        defaultValue = argspec.defaults[i]
      )
      if paramData.has_key(argname):
        d = paramData[argname]
        for key in [ 'shortName', 'description','valueRange', 'valueType',
          'invalidValues', 'validValues', 'endpointInclusion' ]:
          if d.has_key(key): argdetail[key] = d.get(key)
      argdetails.append(argdetail)
      i += 1
      
    expressions[module_name] = dict(
      name = classes[0][0],
      csg = usolid.toData(),
      argdetails = argdetails
    )
    cadmium.inspectionData = dict(solidData={}, paramData={})

  entries = []
  for k, v in expressions.items():
    s = '"'+k+'":{'
    s += '"name":'+'"'+v['name']+'"'+','
    s += '"argdetails":'+json.dumps(v['argdetails'], indent=2)+','
    s += '"csg": function (a) { return '+json.dumps(v['csg'],indent=2)+'}'
    s += '}'
    entries.append(s)

  outtext = '$.templates = {'+',\n\n'.join(entries)+'}'

  open('expressions.js','w').write(outtext)

if __name__ == '__main__':
  main()
