# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# <p><a href="https://zenodo.org/badge/latestdoi/326061406"><img src="https://zenodo.org/badge/326061406.svg"></a>
# <br><img src="https://img.shields.io/badge/platform-osx%20,%20linux-orange">
# <br><img src="https://img.shields.io/badge/language-python3,bash-blue">
# <br><img src="https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet">
# <br><a href="https://travis-ci.com/timm/bnbad2"><img src="https://travis-ci.com/timm/bnbad2.svg?branch=main"></a>
# <br><img src="https://img.shields.io/badge/license-mit-lightgrey"></p><hr>

# Misc python routines. <br>
# (C) 2021 Tim Menzies timm@ieee.org MIT License

import pkg_resources
import random
import pprint
import sys
import re
from .it import *

# -------
# ## Eg : Unit test engine
class Eg:
  egs = {}

  @staticmethod
  def eg(f):
    Eg.egs[f.__name__] = f
    return f

  @staticmethod
  def run(x):
    assert x in Eg.egs, "unknown test function"
    fun = Eg.egs[x]
    try:
      random.seed(1)
      fun()
      print(fun.__name__, "PASS")
    except Exception:
      print(fun.__name__, "FAIL")

  @staticmethod
  def runall(): [Eg.run(x) for x in Eg.egs]


eg = Eg.eg

@eg
def version(): print("Bnbad v2.01")

# ---------
# ## Data in packages

# ------------
# ## csv : read comma-separated file

# Iterate over each none empty line, killing
# whitespace and comments, splitting on commas.
def csv(file, sep=","):
  def prep(x):
    return float if it.less in x or \
        it.more in x or it.num in x else str
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
          line = [(x if x == it.skip else f(x))
                  for f, x in zip(cols, line)]
        yield line

def src(x=None):
  def prep(z):
    z = z if type(z) is str else z.decode("utf-8")
    return z.strip()

  def bytedata():
    for y in x.decode("utf-8").splitlines():
      yield prep(y)

  def strings():
    for y in x.splitlines():
      yield prep(y)

  def csv():
    with open(x) as fp:
      for y in fp:
        yield prep(y)

  def stdin():
    for y in sys.stdin:
      yield prep(y)
  f = strings
  print("xx", x)
  if x is None:
    f = stdio
  elif type(x) is bytes:
    f = bytedata
  elif x[-4:] == ".csv":
    f = csv
  for y in f():
    yield y


@eg
def _csv():
  all = [row for row in csv(it.data + "/weather.csv")]
  assert 15 == len(all)
  assert float == type(all[2][2])
  assert str == type(all[2][0])
  assert 399 == len([row for row in csv(it.data + "/auto93.csv")])
