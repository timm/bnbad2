# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# <a href="https://zenodo.org/badge/latestdoi/326061406"><img src="https://zenodo.org/badge/326061406.svg"></a><br>
# <img src="https://img.shields.io/badge/platform-osx%20,%20linux-orange"><br>
# <img src="https://img.shields.io/badge/language-python3,bash-blue"><br>
# <img src="https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet"><br>
# <a href="https://travis-ci.com/timm/bnbad2"><img src="https://travis-ci.com/timm/bnbad2.svg?branch=main"></a><br>
# <img src="https://img.shields.io/badge/license-mit-lightgrey">
# <hr>

# Stuff to load first, before anything else. <br>
# (C) 2021 Tim Menzies timm@ieee.org MIT License

import argparse
import random
import pprint
import sys
import re

# --------------------
# ## Pretty : classes that can pretty print themselves.

class Pretty:
  def __repr__(i):
    return re.sub(r"'", ' ',
                  pprint.pformat(dicts(i.__dict__), compact=True))

# Converts `i` into a nested dictionary, then pretty-prints that.
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

def ook():
  x = o(a=1, c=o(b=2, c=3))
  assert(x.c.b == x.c.b)

# -----------
# ## items,items : a DSL for system options

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

# Link to Python's ArgParse
def args(f, hello=""):
  p = argparse
  from argparse_color_formatter import ColorHelpFormatter
  lst, b4 = f(), re.sub(r"\n  ", "\n", hello)
  parser = p.ArgumentParser(
      prog="bnbad2",
      description=b4, formatter_class=p.RawDescriptionHelpFormatter)
  [parser.add_argument("-" + key, **args) for key, _, args in lst]
  return parser.parse_args()

# ---------
# ## ok : simple unit test engine

def ok(*l):
  for fun in l:
    try:
      random.seed(1)
      fun()
      print(fun.__name__, "PASS")
    except Exception:
      print(fun.__name__, "FAIL")
