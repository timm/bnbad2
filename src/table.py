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

# Store csv data in a table. <br>
# Summarize rows in columns. <br>
# Define column type and name in row1.<br>
# (C) 2021 Tim Menzies (timm@ieee.org) MIT License

from lib import Pretty
from it import it
import math
import random

# ---------
# ## Columns

# ### Col: super class for colums
class Col(Pretty):
  def __init__(i, pos=0, txt=""):
    i.pos, i.txt, i.n = pos, txt, 0
    i.w = -1 if it.ch.less in txt else 1

  # Add items, increment `n` (if not skipping `x`).
  def add(i, x):
    if x != it.ch.skip:
      i.n += 1
      i.add1(x)
    return x

  # Return the number of bins
  def card(i): return 0

  # Convert `x` to one of a small number of bins.
  def bin(i, x): return x if x == it.ch.skip else i.bin1(i, x)

  # Normalize `x` to a fixed range
  def norm(i, x): return x if x == it.ch.skip else i.norm1(i, x)

  # Default add: no nothing
  def add1(i, x): pass

  # Default bin: just return `x`
  def bin1(i, x): return x

  # Default normalization: just return `x`
  def norm1(i, x): return x

# ### Sym: for columns of symbols
class Sym(Pretty):
  def __init__(i, **d):
    super().__init__(**d)
    i.seen = {}
    i.most, i.mode = 0, None

  def card(i): return len(i.bins())
  def bins(i): return i.seen.keys()

  # Track how many `x` we have seen.
  def add1(i, x):
    new = i.seen(x, 0) + 1
    if new > i.most:
      i.most, i.mode = new, x

# ### Some: for columns of numbers
class Some(Pretty):
  def __init__(i, **d):
    super().__init__(**d)
    i.ok = False
    i.it = o(want=it.some.want,
             min=it.some.min,
             epsilon=it.some.epsilon)
    i._cache, i._bins = [], []

  # Cache up to `i.want` items, selected at random
  def add1(i, x):
    r = random.random
    if i.n < i.it.want: # room for one more
      i.ok = False
      i._cache += [x]
      i._bins = []
    elif r() < i.it.want / i.n: # replace anything, picked at random
      i.ok = False
      i._cache[int(r() * len(i._cache))] = x
      i._bins = []

  # Return the cache, sorted.
  def all(i):
    i._cache = i._cache if i.ok else sorted(i._cache)
    i.ok = True
    return i._cache

  # Return the `p`-th percentile in the cache, bounded
  # from `lo` to `hi`
  def per(i, p=.5, lo=0, hi=None):
    hi = hi or len(i._cache)
    return i.all()[int(lo + p * (hi - lo))]

  # Return the 50-th percentile in the cache, bounded
  # from `lo` to `hi`
  def mid(i, **d): return i.per(p=.5, **d)

  # Return the standard deviation of cache values from lo to hi
  def sd(i, **d): return (i.per(p=.9, **d) - i.per(p=.1, **d)) / 2.54

  # Normalize `x` to the range 0..1
  def norm1(i, x):
    lst = i.all()
    lo, hi = lst[0], lst[-1]
    return (x - lo) / (hi - lo + 1E-32)

  # Return the number of bins
  def card(i): return len(i.bins()) + 1

  # Convert `x` to one of a small number of bins.
  def bin(i, x):
    for n, y in enumerate(i.bins):
      if x <= y:
        return n
    return 1 + len(i.bins)

  # Return the bins.
  def bins(i):
    i._bins = i._bins or i.bins1(i)
    return i._bins

  # Find the bins.
  def bins1(i, x):
    lst = i.all()
    eps = i.sd() * i.it.epsilon
    max = len(lst)
    n = max**i.it.min
    while n < 4 and n < max / 2:
      n = int(n * 1.2)
    hi, lo, b4 = n, 1, 0
    while hi < max - n:
      hi += 1
      if hi - lo > n:
        if lst[hi] - lst[lo] >= eps:
          if b4 == 0 or ((i.mid(lo, hi) - b4) > eps):
            i.bins += lst[hi]
            b4 = i.mid(lo, hi)
            lo = hi
            hi += n

# ---------
# ## Row : storage for one example

class Row(Pretty):
  def __init__(i, lst, t):
    i.dom = 0
    i.cells = [col.add(x) for x, col in zip(lst, t.cols)]
    i.y = None

  # Return the `n`-th column
  def x(i, n): return i.cells[n]

  # Return true if `i` is better than `j`.
  def doms(i, j, t):
    n = len(t.ys)
    s1 = s2 = 0
    for col in t.ys:
      w = col.w
      x, y = i.x(col.pos), i.y(col.pos)
      x, y = col.norm(x), col.norm(y)
      s1 -= math.e**(w * (x - y) / n)
      s2 -= math.e**(w * (y - x) / n)
    return s1 / n < s2 / n

  # pretty print goals
  def show(i, t):
    s = sep = ""
    for col in t.ys:
      s = s + sep + col.txt + "=" + str(i.x(col.pos))
      sep = ". "
    return s

# -------
# ## Table: stores rows, summarized in columns
class Table(Pretty):
  def __init__(i):
    i.it = o(samples=it.table.samples)
    i.xs, i.ys, i.rows, i.cols = [], [], [], []

  # builds a new column, stores it anywhere it needs to be
  def make(i, pos, txt):
    this, btw = Sym, i.xs # default
    if it.ch.less in txt or it.ch.more in txt or it.ch.num in txt:
      this, btw = Some, i.ys
    if it.ch.klass in txt:
      this.btw = Sym, i.ys
    if it.ch.skip in txt:
      this, btw = Col, []
    y = this(pos, txt)
    btw += [y]
    i.cols += [y]

  # Injects a new row of data (and first row creates columns).
  def add(i, lst):
    lst = lst.cells if isinstance(lst, Row) else lst
    if i.cols:
      i.rows += [Row(lst, i)]
    else:
      [i.make(pos, txt) for pos, txt in enumerate(lst)]

  # Over a sample of rows, count how often one row doms another.
  # Set each row's `y` value to the discretized dom count.
  def doms(i):
    some = Some()
    for one in i.rows:
      for _ in range(i.it.samples):
        two = random.choice(i.rows)
        one.dom += one.doms(two)
      some.add(one.dom)
    for one in i.rows:
      one.y = some.bin(some.dom)

  # read table from file
  def read(i, file):
    [i.add(row) for row in csv(file)]
