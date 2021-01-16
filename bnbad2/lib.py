# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# <p><a href="https://zenodo.org/badge/latestdoi/326061406"><img src="https://zenodo.org/badge/326061406.svg"></a>
# <br><img src="https://img.shields.io/badge/language-python3,bash-blue">
# <br><a href="https://badge.fury.io/py/bnbad2"><img src="https://badge.fury.io/py/bnbad2.svg" alt="PyPI version" height="18"></a>
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
  def walk(x):
    assert x in Eg.egs, "unknown test function"
    fun = Eg.egs[x]
    random.seed(1)
    fun()
    print(fun.__name__, "PASS")

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

@ eg
def _csv():
  all = [row for row in csv(it.data + "/weather.csv")]
  assert 15 == len(all)
  assert float == type(all[2][2])
  assert str == type(all[2][0])
  assert 399 == len([row for row in csv(it.data + "/auto93.csv")])

# walk over  data  in buckets of size `n`
def buckets(src, buffer=512):
  def some(lst):
    random.shuffle(lst)
    yield lst
  # --------------------------
  tmp = []
  for x in src:
    tmp += [x]
    if len(tmp) >= buffer:
      for one in some(tmp):
        yield one
      tmp = []
  for one in some(tmp):
    yield one


@eg
def _era():
  buffer = 10
  lst = [i for i in range(40)]
  for n, a in enumerate(buckets(csv(it.data + "/auto93.csv"), buffer=buffer)):
    print("\n", n, a, len(a))

# Incremental stats
class Abcd:
  def __init__(i, db="all", rx="all"):
    i.db = db
    i.rx = rx
    i.yes = i.no = 0
    i.known = {}
    i.a = {}
    i.b = {}
    i.c = {}
    i.d = {}

  def __call__(i, want, got):
    i.knowns(want)
    i.knowns(got)
    if want == got:
      i.yes += 1
    else:
      i.no += 1
    for x in i.known:
      if want == x:
        if got == want:
          i.d[x] += 1
        else:
          i.b[x] += 1
      else:
        if got == x:
          i.c[x] += 1
        else:
          i.a[x] += 1

  def knowns(i, x):
    if not x in i.known:
      i.known[x] = i.a[x] = i.b[x] = i.c[x] = i.d[x] = 0.0
    i.known[x] += 1
    if (i.known[x] == 1):
      i.a[x] = i.yes + i.no

  def header(i):
    print("#", ('{0:20s} {1:11s}  {2:4s}  {3:4s} {4:4s} ' +
                '{5:4s}{6:4s} {7:3s} {8:3s} {9:3s} ' +
                '{10:3s} {11:3s}{12:3s}{13:10s}').format(
        "db", "rx",
        "n", "a", "b", "c", "d", "acc", "pd", "pf", "prec",
        "f", "g", "class"))
    print('-' * 100)

  def ask(i):
    def p(y): return int(100 * y + 0.5)
    def n(y): return int(y)
    pd = pf = pn = prec = g = f = acc = 0
    for x in i.known:
      a = i.a[x]
      b = i.b[x]
      c = i.c[x]
      d = i.d[x]
      if (b + d):
        pd = d / (b + d)
      if (a + c):
        pf = c / (a + c)
      if (a + c):
        pn = (b + d) / (a + c)
      if (c + d):
        prec = d / (c + d)
      if (1 - pf + pd):
        g = 2 * (1 - pf) * pd / (1 - pf + pd)
      if (prec + pd):
        f = 2 * prec * pd / (prec + pd)
      if (i.yes + i.no):
        acc = i.yes / (i.yes + i.no)

      tup = ('{0:20s} {1:10s} {2:4d} {3:4d} {4:4d} ' +
             '{5:4d} {6:4d} {7:4d} {8:3d} {9:3d} ' +
             '{10:3d} {11:3d} {12:3d} {13:10s}')
      print("#", tup.format(i.db,
                            i.rx, n(
                                b + d), n(a), n(b), n(c), n(d),
                            p(acc), p(pd), p(pf), p(prec), p(f), p(g), x))


@eg
def _Abcd():
  import random
  random.seed(1)
  abcd = Abcd(db='randomIn', rx='jiggle')
  train = list('aaaaaaaaaaaaaaaaaaaaaabbbbb')
  test = train[:]
  random.shuffle(test)
  for want, got in zip(train, test):
    abcd(want, got)
  abcd.header()
  abcd.ask()


"""
output:

# db                   rx           n     a    b    c   d    acc pd  pf  prec f  g  class
----------------------------------------------------------------------------------------------------
# randomIn             jiggle       22    1    4    4   18   70  82  80  82  82  32 a
# randomIn             jiggle        5   18    4    4    1   70  20  18  20  20  32 b
"""
