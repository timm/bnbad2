# Find and combine interesting bits. Repeat.<br>
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

# Misc python routines.
# (C) 2021 Tim Menzies timm@ieee.org MIT License

import pprint
import re
import random
import sys
import README as x
print(x.__docstring__)

# Classes that can pretty print themselves.
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
  elif isinstance(i, Thing):
    seen = seen or {}
    if i in seen:
      return "..."
    seen[i] = i
    d = dicts(i.__dict__, seen)
    return d
  else:
    return i

# Fast way to initialize an instance that has no methods.
class o(Pretty):
  def __init__(i, **d): i.__dict__.update(**d)

def ook():
  x = o(a=1, c=o(b=2, c=3))
  assert(x.c.b == x.c.b)

# Iterate over each none empty line, killing
# whitespace and comments, splitting on commas.
def csv(file, sep=","):
  def prep(x):
    return float if it.ch.less in x or \
        it.ch.more in x or it.ch.num in x else str
  linesize = None
  with open(file) as fp:
    for n, line in enumerate(fp):
      line = re.sub(r'([\n\t\r ]|#.*)', '', line.strip())
      if line:
        line = line.split(sep)
        if linesize is None:
          linesize = len(line)
          assert len(line) == linesize,\
              "row size different to header size"
          if n == 0:
            cols = [prep(x) for x in line]
          else:
            line = [f(x) for f, x in zip(cols, line)]
          yield line

'''
## OPTIONS

--asds
  -k 3: low frequency control for payes
  +n: enable fun stuff
--adas
  -m num
  +fred

'''
def help(txt, **d):
  for k, v in d.items():
    pass
  helps[k] = txt
  vs[v] = v

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
    ok(ook)
