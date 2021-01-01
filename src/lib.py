# vim: ts=2 sw=2 sts=2  et :

import pprint
import re
import random
import sys

# Classes that can pretty print themselves.
class Thing:
  def __repr__(i):
    return re.sub(r"'", ' ',
                  pprint.pformat(dicts(i.__dict__), compact=True))

# Converts `i` into a nested dictionary, then pretty-prints that.
def dicts(i, seen=None):
  if isinstance(i, (tuple, list)):
    return [dicts(v, seen) for v in i]
  elif isinstance(i, dict):
    return {k: dicts(i[k], seen) for k in i if str(k)[0] != "_"}
  elif isinstance(i, Thing):
    seen = seen or {}
    j = id(i) % 128021  # ids are LONG; show them shorter.
    if i in seen:
      return f"#:{j}"
    seen[i] = i
    d = dicts(i.__dict__, seen)
    d["#"] = j
    return d
  else:
    return i

# Fast way to initialize an instance that has no methods.
class o(Thing):
  def __init__(i, **d): i.__dict__.update(**d)

def test_o():
  x = o(a=1, c=o(b=2, c=3))
  assert(x.c.b == x.c.b)

# ---------
# Simple unit test engine
def ok(*l):
  for fun in l:
    try:
      fun()
      print("\t", fun.__name__, "PASS")
    except Exception:
      print("\t", fun.__name__, "FAIL")

if __name__ == "__main__":
  if "--test" in sys.argv:
    ok(test_o)
