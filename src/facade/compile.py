
import os
import json
import inspect
import cadmium

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
  expressions[module_name] = dict(
    name = classes[0][0],
    csg = usolid.toData()
  )

open('expressions.js','w').write(json.dumps(expressions, indent=2))
