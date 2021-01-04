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

from .it import *
from .lib import csv, eg
from copy import deepcopy as copy
from collections import defaultdict as sets

class Rule(Pretty):
  def __init__(i, rest=0, best=1, c=c, x=x, nb=nb):
    i.has = sets(dict)
    i.has[c][x] = 1
    i.n = 0
    i.best, i.rest = best, rest
    i.score(nb)

  def score(nb):
    h = nb.h[i.best] + nb.h[i.rest]
    b = nb.like(i.has, i.best, h, 2)
    r = nb.like(i.has, i.rest, h, 2)
    n = b**2 / (b + r)
    i.n = n if b > r + .01 else 0
    return i.n

  def merge(i, j, nb):
    k = copy(i)
    for c in j.has:
      for x in j.has[c]:
        k.has[c][x] = 1
    k.score(nb)
    if k.n > i.n and k.n > j.n:
      return k

  def show(i, t):
    for c in i.has:
      s = s + t.cols[c].txt + " = ("
      sep = ""
      for x in i.has[c]:
        s = s + sep + str(x)
        sep = " or "
      s = s + ") "
    return "[" + str(init(100 * i.n)) + "] " + s

class Nb(Pretty):
  def __init__(i):
    i.it = o(m=it.m, k=it.k, pop=it.pop,
             gen=it.gen, trials=it.trials)
    i.n = 0
    i.best = -1
    i.worst = 1E32
    i.f = sets(dict)
    i.h = sets(lambda: 0)

  def add(i, row, use, t):
    i.n += 1
    h = row.y
    i
