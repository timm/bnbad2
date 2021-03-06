#!/usr/bin/env python3
# vim: filetype=python ts=2 sw=2 sts=2 et :

"""
Optimizer, written as a data miner.  Break the data up into regions
of 'bad' and 'better'. 'Interesting' things occur at very different
frequencies in 'bad' and 'better'. Find interesting bits. Combine
them. Repeat. Nearly all this processing takes log linear time.

     :-------:                 explore  = better==bad
     | Ba    | Bad <----.      planning = max(better - bad)
     |    56 |          |      monitor  = max(bad - better)
     :-------:------:   |      tabu     = min(bad + better)
             | B    |   v       
             |    5 | Better
             :------:

(c) Tim Menzies, 2021
MIT License, https://opensource.org/licenses/MIT. The source code
does not need to be public when a distribution of the software is
made. Modifications to the software can be release under any
license. Changes made to the source code may not be documented.
"""

import argparse
import random
import pprint
import json
import time
import math
import sys
import re

def options(): return ["duo", __doc__,
                       arg("show version", V=False),
                       arg("data dir", data="../data/"),
                       arg("misc seed", seed=1),
                       arg("char for symbols", sym="_"),
                       arg("char for numerics", num=":"),
                       arg("char for more", more=">"),
                       arg("char for less", less="<"),
                       arg("char for skip", skip="?"),
                       arg("char for klass", klass="!"),
                       arg("nb kludge for rare attributes", k=1),
                       arg("nb kludge for rare classes", m=2),
                       arg("contrast lives", lives=128),
                       arg("contrast population", beam=10),
                       arg("some epsilon x", smallx=.35),
                       arg("some epsilon y", smally=.5),
                       arg("some best", best=.80),
                       arg("some want", chop=.5),
                       arg("dom samples", samples=64)]


# -------------------------------
# ## General stuff

# ### Predicates

def nump(z): return the.less in z or the.more in z or the.num in z
def goalp(z): return the.less in z or the.more in z or the.klass in z
def klassp(z): return the.klass in z

# ### Structs

def row(cells): return o(cells=cells, score=0, klass=None)
def data(): return o(rows=[], names=[], cols=cols(), counts=tally())
def cols(): return o(all=things(), x=things(), y=things(),
                     klass=None, w={}, bins={}, goals={})
def things(): return o(all={}, nums={}, syms={})
def tally(): return o(f={}, h={}, n=0)

# ### Misc

# Reset seed
def r0(): random.seed(the.seed)

# Stats from lists (`sd` and `norm` assume sorted data)
def mu(a):
  return sum(a) / len(a) if a else 0
def sd(a):
  return (a[int(.9 * len(a))] - a[int(.1 * len(a))]) / 2.56 if a else 0

def norm(x, a): return max(
    0, min(1, (x - a[0]) / (a[-1] - a[0] + 1E-32)))
def dinc(d, k): x = d[k] = d.get(k, 0) + 1; return x

# Given a list of numerics, report which group holds `x`
def bin(bins, x):
  for n, y in enumerate(bins):
    if x <= y:
      return y
  return math.inf

# Process a certain group of columns; ignore empty cells
def cells(lst, cols):
  lst = lst if isinstance(lst, list) else lst.cells
  for pos, col in cols.items():
    val = lst[pos]
    if val != the.skip:
      yield pos, val, col

# Csv reader. Kill whitespace and comments. Convert
# strings to numbers, it needed.
def csv(file, sep=",", ignore=r'([\n\t\r ]|#.*)'):
  def atom(x):
    try:
      return int(x)
    except Exception:
      try:
        return float(x)
      except Exception:
        return x
  with open(file) as fp:
    for a in fp:
      yield [atom(x) for x in re.sub(ignore, '', a).split(sep)]

# -------------------------------
# ## Ingest
# Creating data tables

def ingest(src):
  data_ = data()
  for lst in src:
    (body if data_.names else head)(data_, lst)
  return footer(data_)

# ### ingest/ head
# Initialize `data.cols`

def head(DATA, LST):
  def head1(pos, txt):
    "Add to  (nums or syms) into (all and (x or y))"
    x = [] if nump(txt) else {}
    if klassp(txt):
      DATA.cols.klass = x
    for z in [DATA.cols.all,
              DATA.cols.y if goalp(txt) else DATA.cols.x]:
      z.all[pos] = x
      (z.nums if nump(txt) else z.syms)[pos] = x
    "Update goal and goal weights."
    if nump(txt) and goalp(txt):
      DATA.cols.goals[pos] = x
      DATA.cols.w[pos] = (-1 if the.less in txt else
                          (1 if the.more in txt else 0))
  # `head` control
  DATA.cols = cols()
  DATA.names = LST
  [head1(i, x) for i, x in enumerate(LST) if the.skip not in x]

# ### ingest / head / body
# Update the column summaries, create new rows.

def body(data, lst):
  "Update symbolics"
  for _, x, c in cells(lst, data.cols.all.syms):
    dinc(c, x)
  "Update numerics"
  for _, x, c in cells(lst, data.cols.all.nums):
    c += [x]
  "Make a new row"
  data.rows += [row(lst)]

# ### ingest / head / footer
# All the stuff to do after reading data

def footer(DATA):
  def classify():
    "klass=TRUE if usually domiante others"
    ys = []
    for row in DATA.rows:
      for _ in range(the.samples):
        row.score += better(row, random.choice(DATA.rows))
      ys += [row.score]
    ys = sorted(ys)
    best = ys[int(the.best * len(ys))]
    for row in DATA.rows:
      row.klass = row.score > best

  def better(i, j):
    "Is row `i` better than row `j`?"
    n = s1 = s2 = 0
    n = len(DATA.cols.goals)
    for pos, col in DATA.cols.goals.items():
      w = DATA.cols.w[pos]
      a, b = i.cells[pos], j.cells[pos]
      a, b = norm(a, col), norm(b, col)
      s1 -= math.e**(w * (a - b) / n)
      s2 -= math.e**(w * (b - a) / n)
    return s1 / n < s2 / n

  def discretize():
    "Split numerics   (uses `div` and `merge`, below."
    for pos, name in enumerate(DATA.names):
      if nump(name) and not goalp(name):
        b4 = div(DATA.cols.x.nums[pos])
        after = merge(pos, DATA.rows, b4)
        print(f"{name:15} :{b4} ==> {after}")
        DATA.cols.bins[pos] = after

  def counts():
    "Summaries DATA via range frequency counts"
    t = DATA.counts
    for row in DATA.rows:
      t.n += 1
      klass = row.klass
      dinc(t.h, klass)
      for pos, x, _ in cells(row, DATA.cols.x.syms):
        v = (klass, DATA.names[pos], x)
        dinc(t.f, v)
      for pos, x, _ in cells(row, DATA.cols.x.nums):
        x = bin(DATA.cols.bins[pos], x)
        v = (klass, DATA.names[pos], x)
        dinc(t.f, v)
  # `footer` control
  [col.sort() for col in DATA.cols.all.nums.values()]
  classify()   # count who dominates who
  discretize() # must be after classify, supervised splits
  counts()     # generate frequency counts
  return DATA


# ------
# ## Discretization

# ### div
# Split sorted list of numbers into bins

def div(lst):
  ok = sd(lst) * the.smallx # sd=10
  n = len(lst)**the.chop
  while n < 4 and n < len(lst) / 2:
    n *= 1.2
  n = int(n)
  out, hi, lo = [], n, 0
  while hi < len(lst) - n:
    hi += 1
    if (hi - lo > n                    # enough left after this split
        and lst[hi] != lst[hi + 1]     # we can split here
            and lst[hi] - lst[lo] > ok): # split is big enough
      out += [lst[hi]]  # collect the split point
      lo, hi = hi, hi + n  # jump to the next split
  return out

# ### merge

def merge(POS, ROWS, BINS):
  def shrink(lst, ok):
    "Combine ranges that make little change to the score."
    j, tmp = 0, []
    while j < len(lst):
      a, y1 = lst[j]
      if j < len(lst) - 1:
        b, y2 = lst[j + 1]
        if abs(mu(y2) - mu(y1)) < ok: # too little different
          tmp += [(b, y1 + y2)] # extend slit to `b`
          j += 2           # jump to next pair
          continue
      tmp += [(a, y1)]
      j += 1
    return shrink(tmp, ok) if len(tmp) < len(lst) else lst

  def grow():
    "Collect the data needed for `shrink`"
    all, ys = {}, []
    for row in ROWS:
      x = row.cells[POS]
      if x != the.skip:
        x = bin(BINS, x)
        one = all[x] = all.get(x, [])
        one += [row.score]
        ys += [row.score]
    return sorted(all.items()), sd(sorted(ys)) * the.smally
  # `merge` control
  return [x[0] for x in shrink(*grow())]

# ------
# ## Contrast set learning

def contrast(rules0, COUNTS, HERE, THERE):
  def loop(rules):
    lives = the.lives
    while True:
      lives -= 1
      total, rules = prune(rules)
      if lives < 1 or len(rules) < 2:
        return rules
      rules += [combine(pick(rules, total), pick(rules, total))]

  def value(rule):
    b = like(rule, HERE, 2)
    r = like(rule, THERE, 2)
    return b**2 / (b + r) if b > r else 0

  def like(rule, h, hs=None):
    hs = hs if hs else len(COUNTS.h)
    like = prior = (COUNTS.h[h] + the.k) / (COUNTS.n + the.k * hs)
    like = math.log(like)
    for col, values in rule:
      f = sum(COUNTS.f.get((h, col, v), 0) for v in values)
      inc = (f + the.m * prior) / (COUNTS.h[h] + the.m)
      like += math.log(inc)
    return math.e**like

  def combine(rule1, rule2):
    _, rule1 = rule1
    _, rule2 = rule2
    tmp = dict()
    for rule in [rule1, rule2]:
      for k, lst in rule:
        tmp[k] = tmp.get(k, set())
        for v in lst:
          tmp[k].add(v)
    rule3 = sorted([[k, sorted(list(vs))] for k, vs in tmp.items()])
    return [value(rule3), rule3]

  def same(rule1, rule2):
    if rule1[0] != rule2[0]:
      return False
    for x, y in zip(rule1[1], rule2[1]):
      if x != y:
        return False
    return True

  def prune(old):
    ordered = [[s, r] for s, r in sorted(old, reverse=True)]
    one = ordered[0]
    unique = [one]
    for two in ordered[1:]:
      if not same(one, two):
        unique += [two]
      one = two
    pruned = [[s, r] for s, r in unique if s > 0][:the.beam]
    return sum(s for s, _ in pruned), pruned

  def pick(rules, total):  # (s1, r1) (s2,r2) (s3,r3) total=s1+s2+s3
    r = random.random()
    for rule in rules:
      r -= rule[0] / total
      if r <= 0:
        return rule
    return rule
  # `contrast` control
  return loop([[value(r), r] for r in rules0])

def learn(counts):
  out, all = {}, list(set([(c, x) for (_, c, x) in counts.f]))
  for there in counts.h:
    for here in counts.h:
      if here != there:
        out[here] = contrast([[[c, [x]]] for c, x in all],
                             counts, here, there)
  return out

def showRule(r):
  def show1(k, v):
    return k + " = (" + ' or '.join(map(str, v)) + ")"
  s, rule = r
  out = ""
  return "{" + str(round(s, 2)) + '} ' + ' and '.join([show1(k, v) for k, v in rule])

# ---------------------


def printm(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)

def arg(txt, **d):
  for key, val in d.items():
    break
  x = val[0] if isinstance(val, list) else val
  if val is False:
    return key, x, dict(help=txt, action='store_true')
  else:
    m, t = "S", str
    if isinstance(x, int):
      m, t = "I", int
    if isinstance(x, float):
      m, t = "F", float
    if isinstance(val, list):
      return key, x, dict(help=txt, choices=val, x=x, metavar=m, type=t)
    else:
      eg = "; e.g. -%s %s" % (key, val) if val != "" else ""
      return key, x, dict(help=txt + eg, default=x, metavar=m, type=t)

def about(what, txt, *lst):
  return o(** {key: x for key, x, _ in lst})

def args(what, txt, *lst):
  p = argparse
  from argparse_color_formatter import ColorHelpFormatter
  parser = p.ArgumentParser(
      prog=what, description=txt,
      formatter_class=p.RawDescriptionHelpFormatter)
  [parser.add_argument("-" + key, **args) for key, _, args in lst]
  return parser.parse_args()


def subsets(s, max=None):
  max = max if max else len(s)
  for cardinality in range(max + 1):
    yield from combinations(s, cardinality)

class Pretty:
  def __repr__(i):
    return re.sub(r"'", ' ',
                  pprint.pformat(dicts(i.__dict__), compact=True))

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

# ---
# pretties
class zing:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

  def header(x): print(zing.HEADER + x + zing.ENDC)
  def okblue(x): print(zing.OKBLUE + x + zing.ENDC)
  def okcyan(x): print(zing.OKCYAN + x + zing.ENDC)
  def okgreen(x): print(zing.OKGREEN + x + zing.ENDC)
  def warning(x): print(zing.WARNING + x + zing.ENDC)
  def fail(x): print(zing.FAIL + zing.BOLD + x + zing.ENDC)


def neg(f): return f

def run(f): f(); return f

def eg(f):
  zing.header("# " + f.__name__)
  try:
    f()
  except Exception:
    ok(False, "function ran?")
  return f

def ok(x, txt=""):
  if x:
    print("\t" + txt + zing.OKGREEN + " PASS" + zing.ENDC)
  else:
    print("\t" + txt + zing.FAIL + " FAIL" + zing.ENDC)


# ---------------------
# ## Start up stuff
the = args(*options())

# -------------------------------------
# tests
# @eg
def _csv():
  all = [row for row in csv(the.data + "weather.csv")]
  ok(len(all) == 15, "csv reads?")
  ok(len(all[-1]) == 5, "rows read?")
  ok(type(all[-1][1]) == float, "floats read?")
  ok(type(all[-1][0]) == str, "strings read?")

# @eg
def aa():
  r0()
  d = ingest(csv(the.data + "auto93.csv"))
  rows = sorted(d.rows, key=lambda z: z.score)
  printm([['score'] + d.names] + [
      [r.score] + r.cells for r in rows[:5]] + [
      [r.score] + r.cells for r in rows[-5:]])

# [[name,ranges]...
def relevants(data, rule):
  what = {name: col for col, name in enumerate(data.names)}

  def relevant(row, ands):
    for name, ranges in ands:
      col = what[name]
      x = row.cells[col]
      if x != the.skip:
        x = bin(data.cols.bins[col],
                x) if col in data.cols.bins else x
        if x not in ranges:
          return False
    return True
  return sorted([row.score for row in data.rows
                 if relevant(row, rule[1])])

def _contrast():
  r0()
  d = ingest(csv(the.data + "auto93.csv"))
  c0 = None
  all = sorted(
      list(set([(c, x) for (_, c, x) in d.counts.f if not nump(c)])))
  for c, x in all:
    if c != c0:
      print(f"\n{c:15} :[", end="")
    print(f" {x}", end="")
    c0 = c
  print("]")
  return d, learn(d.counts)


if __name__ == "__main__":
  the = args(*options())
  print(the.seed)
  r0()
  import pprint
  d, cons = _contrast()
  b4 = sorted(row.score for row in d.rows)
  print("b4", round(mu(b4), 2), round(sd(b4), 2))
  for k, rules in cons.items():
    print("\nhow to get to", k)
    [print("  ", showRule(rule)) for rule in rules]
    for rule in rules:
      after = relevants(d, rule)
      print("after", round(mu(after), 2), round(sd(after), 2))
