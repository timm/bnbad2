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


the = o(rowsamples=64,
        best=0.67,
        ysmall=.2,
        xsmall=.2,
        xchop=.5)

def Tbl(rows=[]): return o(cols={}, x={}, y={}, rows=rows)
def Row(cells=[]): return o(cells=cells, score=0, klass=True)
def Col(txt='', pos=0, w=1):
  return o(n=0, txt=txt, pos=pos, has=None, spans=[],
           w=-1 if "<" in txt else 1)
def Span(lo=-math.inf, hi=math.inf, has=None):
  return o(lo=lo, hi=hi, _has=has if has else [])
def Counts(): return o(f={}, h={})


def table(src, tbl=None):
  def discretize(tbl):
    def pairs(lst, fx, fy):
      xs, ys, xy = [], [], []
      for one in lst:
        x = fx(one)
        if x != "?":
          y = fy(one)
          xs += [x]
          ys += [y]
          xy += [(x, y)]
      return (sd(sorted(xs)) * the.xsmall, sd(sorted(ys)) * the.ysmall,
              sorted(xy))
    for col in tbl.x.values():
      if numsp(col.has):
        col.spans = div(*pairs(tbl.rows,
                               lambda z: z.cells[col.pos],
                               lambda z: z.score))

  def classify(tbl):
    def better(tbl, row1, row2):
      s1, s2, n = 0, 0, len(tbl.y)
      for col in tbl.y.values():
        pos, w = col.pos, col.w
        a, b = row1.cells[pos], row2.cells[pos]
        a, b = norm(col.has, a), norm(col.has, b)
        s1 -= math.e**(w * (a - b) / n)
        s2 -= math.e**(w * (b - a) / n)
      return s1 / n < s2 / n
    #######################
    for row1 in tbl.rows:
      row1.score = sum(better(tbl, row1, choice(tbl.rows))
                       for _ in range(the.rowsamples))
    for n, row in enumerate(sorted(tbl.rows,
                                   key=lambda z: z.score)):
      row.klass = n > len(tbl.rows) * the.best

  def head(tbl, x):
    for pos, txt in enumerate(x):
      if not "?" in txt:
        tbl.cols[txt] = tmp = Col(txt, pos)
        if "<" in txt or ">" in txt or "!" in txt:
          tbl.y[txt] = tmp
        else:
          tbl.x[txt] = tmp

  def body(tbl, x):
    def inc(col, x):
      if col.has is None:
        col.has = [] if isa(x, (float, int)) else {}
        return inc(col, x)
      col.n += 1
      if symsp(col.has):
        col.has[x] = col.has.get(x, 0) + 1
      else:
        col.has += [x]
    [inc(c, x[c.pos]) for c in tbl.cols.values() if x[c.pos] != "?"]
    tbl.rows += [Row(x)]

  def footer(tbl):
    for col in tbl.cols.values():
      if numsp(col.has):
        col.has.sort()
    classify(tbl)
    discretize(tbl)
  ##########################
  tbl = tbl if tbl else Tbl()
  for x in src:
    (body if len(tbl.cols) else head)(tbl, x)
  footer(tbl)
  return tbl

def div(xsmall, ysmall, xy):
  def merge(b4):
    j, now = 0, []
    while j < len(b4):
      a = b4[j]
      if j < len(b4) - 1:
        b = b4[j + 1]
        if abs(mu(b._has) - mu(a._has)) < ysmall:
          merged = Span(lo=a.lo, hi=b.hi, has=a._has + b._has)
          now += [merged]
          j += 2
      now += [a]
      j += 1
    return merge(now) if len(now) < len(b4) else now
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
            and span.hi - span.lo > xsmall):
      span._has = [z[1] for z in xy[b4:now]]
      tmp += [span]
      span = Span(lo=xy[now][0])
      b4 = now
      now += n
  tmp += [Span(lo=xy[b4][0], hi=xy[-1][0],
               has=[z[1] for z in xy[b4:]])]
  out = merge(tmp)
  out[0].lo = -math.inf
  out[-1].hi = math.inf
  return out


def counts(tbl):
  out = Counts()
  for row in tbl.rows:
    k = row.klass
    out.h[k] = out.h.get(k, 0) + 1
    for col in tbl.x.values():
      x = row.cells[col.pos]
      if x != "?":
        x = bin(col.spans, x) if numsp(col.has) else x
        v = (k, col.txt, col.pos, x)
        out.f[v] = out.f.get(v, 0) + 1
  return out

# ## Misc utilties

def mu(lst): return sum(lst) / len(lst)
def norm(lst, x): return (x - lst[0]) / (lst[-1] - lst[0] + 1E-32)
def sd(lst): return (
    lst[int(.9 * len(lst))] - lst[int(.1 * len(lst))]) / 2.56

def bin(spans, x):
  for span in spans:
    if span.lo <= x < span.hi:
      return span.hi
  return span.hi


isa = isinstance
def numsp(x): return isa(x, list)
def symsp(x): return isa(x, dict)

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


print([r for r in csv("../data/weather.csv")])

# for k, v in counts(table(csv("../data/auto93.csv"))).f.items():
# print(k, v)
