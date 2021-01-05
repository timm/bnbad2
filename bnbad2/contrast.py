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

class Rule(Pretty):
  def __init__(i, rest, best, c, x, nb):
    i.has = sets(dict)
    s = set()
    i.x0 = x
    s.add(x)
    i.has[c] = s
    i.n = 0
    i.best, i.rest = best, rest
    i.score(nb)

  # Return likelihood that `has` belongs to `best`
  # much more that `rest`..
  def score(nb):
    all = nb.h[i.best] + nb.h[i.rest]
    b = nb.like(i.has, i.best, all, 2)
    r = nb.like(i.has, i.rest, all, 2)
    n = b**2 / (b + r)
    i.n = n if b > r + .01 else 0
    return i.n

  # Return a better rule, or None.
  def better(i, j, nb):
    k = copy(i)
    [k.has[c].add(x) for c in j.has]
    k.score(nb)
    if k.n > i.n and k.n > j.n:
      return k

  def same(i, j):
    return i.n == j.n and i.has == j.has

  # Pretty print for a row.
  def show(i, t):
    for c in i.has:
      s = s + t.cols[c].txt + " = ("
      sep = ""
      for x in i.has[c]:
        s = s + sep + str(x)
        sep = " or "
      s = s + ") "
    return "[" + str(init(100 * i.n)) + "] " + s

# -----------------
# ### Nb : Reason about frequency counts

class Nb(Pretty):
  def __init__(i):
    i.it = o(m=it.m, k=it.k, pop=it.pop,
             gen=it.gen, trials=it.trials)
    i.n = 0
    i.best = -1
    i.worst = 1E32
    i.f = {} # count the (hypothesis,column,value)
    i.h = {}

  # For everything in `cols`,
  # update frequency counts (from `row`)
  def add(i, row, cols):
    i.n += 1
    h = row.y
    i.h[h] = i.h[h].get(h, 0) + 1
    i.worst = h if h < i.worst else i.worst
    i.best = h if h > i.best else i.best
    for c in cols:
      x = row.x(c.pos)
      if x != it.skip:
        x = c.bin(x)
        v = (h, c, x)
        i.f[v] = i.f.get(v, 0) + 1

  # Return likelihood that `thing` belongs to `h`.
  def like(i, thing, h, all, hs):
    like = prior = (i.h[h] + i.it.k) / (all + i.k * hs)
    like = math.log(like)
    for c in thing:
      f = sum(i.f.get((h, c, v), 0) for v in thing[c])
      inc = (f + i.it.m * prior) / (i.h[h] + i.it.m)
      like += math.log(inc)
    return math.e**like

  # Return rules listing ranges that are low frequency
  # in `rest` and high frequency in `i.best`
  def rules(i, t):
    all = {}
    for rest in i.h:
      if rest != i.best:
        lst = []
        for col in t.xs:
          tmp = [Rule(rest, i.best, c, x, i) for x in col.range()]
          if type(col) == Some:
            tmp = i.merge(sorted(tmp, key=lambda z: z.x0))
          lst += i.prune(tmp)
        all[rest] = i.learn(lst, i.it.gen)
    return all

  # Try to merge adjacent rules.
  # If  anything merges, then repeat.
  def merge(i, lst):
    shorter = False
    j, tmp, max = 0, [], len(lst)
    while j < max:
      a = lst[j]
      if j < max - 1:
        b = lst[j + 1]
        if c := a.better(b):
          shorter = True
          a = c
          j += 1
      tmp += [a]
      j += 1
    return i.merge(tmp) if shorter else lst

  # Sort descending by value, remove lesser valuable items,
  # Remove duplicates (which, after sorting, will be adjacent).
  def prune(i, rules):
    tmp = sorted(rules, key=lambda z: -1 * z.n)[:i.it.pos]
    b4 = tmp[0]
    out = [b4]
    for now in tmp[1:]:
      if not b4.same(now):
        out += [now]
      b4 = now
    return out

  # A couple of times, combine two rules. If
  # that produces anything better than before,
  # recurse to try it all again.
  def learn(i, rules, gen):
    if gen < 2 or len(rules) < 2:
      return rules
    rules = i.prune(rules)
    total = sum(rule.n for rule in rules)
    more = []
    for _ in range(i.it.samples):
      one = i.one(rules, total)
      two = i.one(rules, total)
      if new := one.better(two, i):
        more += [new]
    if more:
      rules += more
      return i.learn(rules, gen - 1)

  # Pick a rule, favoring things with higher value.
  def one(rules, total):
    r = random.random()
    for rule in rules:
      r -= rule.n / total
      if r <= 0:
        return rule
    return rule
