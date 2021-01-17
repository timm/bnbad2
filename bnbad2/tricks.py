import argparse
import random
import pprint
import math
import sys
import re

def arg(txt, **d):
  for key, val in d.items():
    break
  x = val[0] if isinstance(val, list) else val
  if val is False:
    return key, x, dict(help=txt, action='store_true')
  else:
    m, t = "S", str
    if isinstance(x, int):
      m, t = "I", int
    if isinstance(x, float):
      m, t = "F", float
    if isinstance(val, list):
      return key, x, dict(help=txt, choices=val, x=x, metavar=m, type=t)
    else:
      eg = "; e.g. -%s %s" % (key, val) if val != "" else ""
      return key, x, dict(help=txt + eg, default=x, metavar=m, type=t)

def args(what, txt, *lst):
  p = argparse
  from argparse_color_formatter import ColorHelpFormatter
  parser = p.ArgumentParser(
      prog=what, description=txt,
      formatter_class=p.RawDescriptionHelpFormatter)
  [parser.add_argument("-" + key, **args) for key, _, args in lst]
  return parser.parse_args()

def neg(f): return f
def eg(f): f(); return f
def ok(x, txt=""): print(txt, ("PASS" if x else "FAIL"))

class Pretty:
  def __repr__(i):
    return re.sub(r"'", ' ',
                  pprint.pformat(dicts(i.__dict__), compact=True))

def dicts(i, seen=None):
  if isinstance(i, (tuple, list)):
    return [dicts(v, seen) for v in i]
  elif isinstance(i, dict):
    return {k: dicts(i[k], seen) for k in i if str(k)[0] != "_"}
  elif isinstance(i, Pretty):
    seen = seen or {}
    if i in seen:
      return "..."
    seen[i] = i
    d = dicts(i.__dict__, seen)
    return d
  else:
    return i

# ------------
# ## o : simple structs

# Fast way to initialize an instance that has no methods.
class o(Pretty):
  def __init__(i, **d): i.__dict__.update(**d)
