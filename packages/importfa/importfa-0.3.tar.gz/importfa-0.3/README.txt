Given an equivalent way to achieve this but in import style, prevent formatter smash up your code

```
import xxx
if __name__=="__main__":
    import os,sys
    fa = os.path.abspath("/".join([sys.argv[0] + "/.."] + [".."] * 2))
    sys.path.append(fa)

import xxx_local_package # similar to ..xxx
```

For short, this project does this:

| use this project    |     |  equivalent code  |
| --- | --- | --- |
| import importfa.f | → | os.path.append(sys.argv\[0\] + "/../..") |
| import importfa.ff | →  | os.path.append(sys.argv\[0\] + "/../../..") |
| import importfa.fff |  → | os.path.append(sys.argv\[0\] + "/../../../..") |
| import importfa.fffff |  →  | os.path.append(sys.argv\[0\] + "/../../../../..") |


For convenience, `import importfa.f8` is  equivalent to `importfa.ffffffff`,etc.