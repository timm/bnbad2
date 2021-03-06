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

import math
from .it import *
from .lib import csv, eg
from copy import deepcopy as copy
from .table import Some

class Explore(Pretty):
  def __init__(i, file):
    i.it = o(k=it.k, m=it.m, wait=it.wait, buffer=it.buffer)

  def read(file):
    train, test = [], []
    header = None
    for n, test in enumerate(buckets(csv(file), buffer=i.it.buffer)):
      while test:
        if not header:
          header = test.pop()
        else:
          if n >= i.it.wait:
            test = i.rank([header] + train, test)
          train += [test.pop()]

  def rank(header, train, test):
    tab = Table()
    [tab.add(x) for x in train]
    tab.doms()
    [col.merge(tab) for col in tab.xs]
