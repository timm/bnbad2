# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# [![DOI](https://zenodo.org/badge/318809834.svg)](https://zenodo.org/badge/latestdoi/318809834)<br>
# ![](https://img.shields.io/badge/platform-osx%20,%20linux-orange)<br>
# ![](https://img.shields.io/badge/language-python3,bash-blue)<br>
# ![](https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet)<br>
#  [![Build Status](https://travis-ci.com/timm/bnbad2.svg?branch=main)](https://travis-ci.com/timm/bnbad2)<br>
# ![](https://img.shields.io/badge/license-mit-lightgrey)
# --------

# Stuff to load first, before anything else. <br>
# (C) 2021 Tim Menzies timm@ieee.org MIT License

import pprint
import re
import random
import sys

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

# For an example  of this DSL, see [it](it.html).

def item(txt, **d):
  for key, default in d.items():
    return o(key=key, default=default, txt=txt)

def items(x):
  if isinstance(x, list):
    return o(**{y.key: items(y.default) for y in x})
  else:
    return x

def helptext(lst):
  def pad(x, n=20, c=" "): return x.ljust(n, c)
  for group in lst:
    print(pad("\n-" + group.key + " ", c=".") + " " + group.txt)
    for x in group.default:
      if x.default == False:
        pre = "+" + x.key
      else:
        pre = "-" + x.key + " " + str(x.default)
      print("   " + pad(pre, n=17) + x.txt)

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
