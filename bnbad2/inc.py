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
def Span(lo=-math.inf, hi=math.inf, has=None):
  return o(lo=lo, hi=hi, ys=ys if ys else [])

def mu(lst): return sum(lst) / len(lst)

def norm(lst, x):
  return (x - lst[0]) / (lst[-1] - lst[0] + 1E-32)

def sd(lst):
  n = len(lst)
  return (lst[int(.9 * n)] - a[int(.1 * n)]) / 2.56


isa = isinstance

def inc(col, x):
  if col.has is None:
    col.has = [] if isa(x, (float, int)) else {}
    return inc(col, x)
  col.n += 1
  if isa(col.has, dict):
    dct = cols.has
    dct[x] = dct.get(x, 0) + 1
  else:
    lst = col.has
    if len(lst) < the.some:
      lst += [x]
    elif r() < the.colsamples / col.n:
      lst[int(r() * len(lst))] = x

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

def pairs(tbl, colx, coly):
  def val(col, row): return row.cells[col.pos]
  return (sd(sorted(colx.has)) * the.xsmall,
          sd(sorted(colx.has)) * the.ysmall,
          sorted([(val(colx, r), val(coly, r)) for r in rows
                  if val(colx, r) != "?"]))

def div(xok, yok, xy):
  def merge(b4, yok):
    j, now = 0, []
    while j < len(b4):
      a = b4[j]
      if j < len(b4) - 1:
        b = b4[j + 1]
        if abs(mu(b.has) - mu(a.has)) < yok:
          merged = Span(lo=a.lo, hi=b.hi, has=a.has + b.has)
          now += [merged]
          j += 2
      now += [a]
      j += 1
    return merge(now, yok) if len(now) < len(b4) else now
  # -----------------------------
  n = len(xy)**the.xchop
  while n < 4 and n < len(xy) / 2:
    n *= 1.2
  n, tmp, b4, span = int(n), [], 0, Span(lo=xy[0][0])
  now = n
  while now < len(xy) - n:
    x = xy[now][0]
    span.hi = x
    now += 1
    if (now - b4 > n and now < len(xy) - 2
            and x != xy[now][0]
            and span.hi - span.lo > xok):
      span.has = [z[1] for z in xy[b4:now]]
      tmp += [span]
      span = Span(lo=xy[now])
      b4 = now
      now += n
  tmp += [Span(lo=xy[b4][0], hi=xy[-1][0],
               ys=[z[1] for z in xy[b4:]])]
  out = merge(tmp, yok)
  out[0].lo = -math.inf
  out[-1].hi = math.inf
  return out

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
