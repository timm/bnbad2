# Find and combine interesting bits. Repeat.
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html) 
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/tim/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# [![DOI](https://zenodo.org/badge/318809834.svg)](https://zenodo.org/badge/latestdoi/318809834)  
# ![](https://img.shields.io/badge/platform-osx%20,%20linux-orange)    
# ![](https://img.shields.io/badge/language-python3,bash-blue)  
# ![](https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet)  
#  [![Build Status](https://travis-ci.com/timm/bnbad2.svg?branch=main)](https://travis-ci.com/timm/bnbad2)   
# ![](https://img.shields.io/badge/license-mit-lightgrey)
# --------

it = dict(what    = "Misc python routines",
          who     = "Tim Menzies",
          when    = "2021",
          license = "MIT License")

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
    if i in seen: return "..."
    seen[i] = i
    d = dicts(i.__dict__, seen)
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
