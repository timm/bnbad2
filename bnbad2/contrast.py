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

# ## Rule : thing that stores ranges
class Rule(Pretty):
  def __init__(i, rest, best, c, x, nb):
    i.x0 = x
    s = set()
    s.add(x)
    i.has = {}
    i.has[c] = s
    i.n = 0
    i.best, i.rest = best, rest
    i.score(nb)

  # Return likelihood that `has` belongs to `best`
  # much more that `rest`..
  def score(i, nb):
    all = nb.h[i.best] + nb.h[i.rest]
    b = nb.like(i.has, i.best, all, 2)
    r = nb.like(i.has, i.rest, all, 2)
    n = b**2 / (b + r)
    i.n = n if b > r + .01 else 0
    return i.n

  # Return a better rule, or None.
  def better(i, j, nb):
    k = copy(i)
    for c in j.has:
      k.has[c] = k.has.get(c, set())
      for x in j.has[c]:
        k.has[c].add(x)
    k.score(nb)
    if k.n > i.n and k.n > j.n:
      return k

  def same(i, j):
    return i.n == j.n and i.has == j.has

  # Pretty print for a row.
  def show(i, t):
    s = pre = ""
    for c in i.has:
      s = s + pre + t.cols[c].txt + " = ("
      pre = " and "
      sep = ""
      for x in i.has[c]:
        s = s + sep + str(x)
        sep = " or "
      s = s + ")"
      if type(t.cols[c]) == Some:
        s = s + "/" + str(t.cols[c].card())
      s = s + " "
    return "[" + str(int(100 * i.n)) + "] " + s

@ eg
def _rule():
  from .table import Table
  t = Table().read(it.data + "/auto93.csv")
  t.doms()
  for c in t.xs:
    if type(c) == Some:
      print("bins", c.txt, c.bins())
  p = Nb()
  [p.add(row, t.xs, t.ys) for row in t.rows]
  p.show()
  for cluster, rules in p.rules(t).items():
    print("\n")
    for rule in rules:
      if rule.n > 0:
        print(cluster, rule.show(t))
  #
  # for x in p.f: print(x, p.f[x])
  # -----------------
# ### Nb : Reason about frequency counts

class Nb(Pretty):
  def __init__(i):
    i.it = o(m=it.m, k=it.k, pop=it.pop, lives=it.lives,
             attempts=it.attempts)
    i.n = 0
    i.best = -1
    i.worst = 1E32
    i.f = {} # count the (hypothesis,column,value)
    i.h = {}
    i.log = {}

  # For everything in `cols`,
  # update frequency counts (from `row`)
  def add(i, row, cols, goals):
    i.n += 1
    i.addx(row, row.y, cols, goals)
    i.addy(row, row.y, cols, goals)
    return i

  def addx(i, row, h, cols, goals):
    for c in cols:
      x = row.x(c.pos)
      if x != it.skip:
        x = c.bin(x)
        v = (h, c.pos, x)
        i.f[v] = i.f.get(v, 0) + 1

  def addy(i, row, h, cols, goals):
    i.h[h] = i.h.get(h, 0) + 1
    i.worst = h if h < i.worst else i.worst
    i.best = h if h > i.best else i.best
    if h not in i.log:
      i.log[h] = [Some(txt=c.txt, pos=c.pos) for c in goals]
    for one in i.log[h]:
      one.add(row.x(one.pos))

  def show(i):
    for h in sorted(h for h in i.log):
      print(h, ', '.join([one.show() for one in i.log[h]]))

# Return likelihood that `thing` belongs to `h`.
  def like(i, thing, h, all, hs):
    like = prior = (i.h[h] + i.it.k) / (all + i.it.k * hs)
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
          tmp = [Rule(rest, i.best, col.pos, x, i)
                 for x in col.range()]
          if type(col) == Some:
            tmp = i.merge(sorted(tmp, key=lambda z: z.x0))
          lst += tmp
        all[rest] = i.learn(lst, i.it.lives)
    return all

  # Try to merge adjacent rules.
  # If  anything merges, then repeat.
  def merge(i, b4):
    j, now, max = 0, [], len(b4)
    while j < max:
      a = b4[j]
      if j < max - 1:
        b = b4[j + 1]
        if c := a.better(b, i):
          now += [c]
          j += 2
          continue
      now += [a]
      j += 1
    return i.merge(now) if len(now) < len(b4) else b4

  # Sort descending by valuLe, remove lesser valuable items,
  # Remove duplicates (which, after sorting, will be adjacent).
  def prune(i, rules):
    tmp = sorted(rules, key=lambda z: -1 * z.n)[:i.it.pop]
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
  def learn(i, rules, lives):
    rules = i.prune(rules)
    print(".", end="")
    if lives < 0 or len(rules) < 2:
      return rules
    total = 1E-32 + sum(rule.n for rule in rules)
    more = []
    for _ in range(i.it.attempts):
      one = i.one(rules, total)
      two = i.one(rules, total)
      if new := one.better(two, i):
        more += [new]
    if more:
      rules += more
      return i.learn(rules, lives - 1)
    else:
      print("!")
      return rules

  # Pick a rule, favoring things with higher value.
  def one(i, rules, total):
    r = random.random()
    for rule in rules:
      r -= rule.n / total
      if r <= 0:
        return rule
    return rule
