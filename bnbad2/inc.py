# vim: filetype=python ts=2 sw=2 sts=2 et :

import argparse
from random import random as r
from random import seed as seed
from random import choice as choice
import time
import math
import sys
import re

class o():
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return str(
      {k: v for k, v in sorted(i.__dict__.items()) if str(k)[0] != "_"})


the = o(colsamples=32, rowsamples=64, best=0.75, xsmall=.35, xchop=.5)

def Tbl(rows=[]): return o(cols={}, x={}, y={}, rows=rows)
def Row(cells=[]): return o(cells=cells, score=0, klass=True)
def Col(txt='', pos=0, w=1):
  return o(n=0, txt=txt, pos=pos, has=None,
           w=-1 if "<" in txt else 1)
def Nums(): return o(all=[], sorted=False)
def Span(lo=-math.inf, hi=math.inf): return o(lo=lo, hi=hi, has=Nums())

def ordered(i):
  i.all = i.all if i.sorted else sorted(i.all)
  i.sorted = True
  return i.all


def symsp(x): return isinstance(x, dict)
def numsp(x): return isinstance(x, list)
def nump(x): return isinstance(x, (float, int))

def inc(col, x):
  if col.has is None:
    col.has = Nums() if nump(x) else {}
    return inc(col, x)
  col.n += 1
  if symsp(col.has):
    col.has[x] = col.has.get(x, 0) + 1
  else:
    if len(col.has.all) < the.colsamples:
      col.has.all += [x]
      col.has.sorted = False
    elif r() < the.colsamples / col.n:
      col.has.all[int(r() * len(col.has.all))] = x
      col.has.sorted = False

def mu(ord): return sum(ord.all) / len(ord.all)

def norm(ord, x):
  a = ordered(ord)
  return (x - a[0]) / (a[-1] - a[0] + 1E-32)

def sd(i):
  a = ordered(i)
  return (a[int(.9 * len(a))] - a[int(.1 * len(a))]) / 2.56

def better(tbl, row1, row2):
  s1, s2, n = 0, 0, len(tbl.y)
  for col in tbl.y.values():
    pos, w = col.pos, col.w
    a, b = row1.cells[pos], row2.cells[pos]
    a, b = norm(col.has, a), norm(col.has, b)
    s1 -= math.e**(w * (a - b) / n)
    s2 -= math.e**(w * (b - a) / n)
  return s1 / n < s2 / n

def classify(tbl):
  for row1 in tbl.rows:
    row1.score = sum(better(tbl, row1, choice(tbl.rows))
                     for _ in range(the.rowsamples))
  for n, row in enumerate(sorted(tbl.rows, key=lambda z: z.score)):
    row.klass = n > len(tbl.rows) * the.best
  return tbl

def div(tbl, x, y):
  xok = sd(x.has) * the.xsmall
  n = x.n**the.xchop
  while n < 4 and n < len(lst) / 2:
    n *= 1.2
  n, out, there, span = int(n), [], 0, Span()
  rows = sorted(tbl.rows, key=lambda z: z.cells[xcol.pos])
  for here, row in enumerate(rows):
    yval = row.cells[y.pos]
    xval = row.cells[x.pos]
    if xval != "?":
      span.hi = xval
      inc(span.has, yval)
      if (here - there > n                    # enough left after this split
                  and here < len(tbl.rows) - 2
                  and xval != rows[here + 1].cells[x.pos]
                  and span.hi - span.lo > xok
              ):
        out += [span]
        span = Span(lo=xval)
        there = here
  return merge(out, sd(y.has) * the.ysmall)

def merge(lst, yok):
  j, tmp = 0, []
  while j < len(lst):
    a = lst[j]
    if j < len(lst) - 1:
      b = lst[j + 1]
      if abs(mu(b.has) - mu(a.has)) < yok:
        merged = Span(lo=a.lo, hi=b.hi)
        for x in a.has + b.has:
          inc(merged.has, x)
        tmp += [merged]
        j += 2
    tmp += [a]
    j += 1
  return merge(tmp, yok) if len(tmp) < len(lst) else tmp

  # a certain group of columns; ignore empty cells
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

def head(t, x):
  for pos, txt in enumerate(x):
    if not "?" in txt:
      t.cols[txt] = tmp = Col(txt, pos)
      if "<" in txt or ">" in txt or "!" in txt:
        t.y[txt] = tmp
      else:
        t.x[txt] = tmp

def body(t, x):
  [inc(c, x[c.pos]) for c in t.cols.values() if x[c.pos] != "?"]
  t.rows += [Row(x)]

def table(src, t=None):
  t = t if t else Tbl()
  for x in src:
    (body if len(t.cols) else head)(t, x)
  return t


# cols["_cylinders"])
classify(table(csv("../data/auto93.csv"))).rows


def pick(l, samples=100):
  l = sorted(l, reverse=True)
  n = sum(x[0] for x in l)
  for _ in range(samples):
    m = r()
    for s, out in l:
      m -= s / n
      if m < 0:
        yield out
    yield out

def test_pick():
  seed(1)
  d = {}
  n = 0
  for x in pick([(4, "a"), (2, "b"), (1, "c")]):
    n += 1
    d[x] = d.get(x, 0) + 1
  print({k: v / n for k, v in d.items()})
  print(1 / 7, 2 / 7, 4 / 7)
