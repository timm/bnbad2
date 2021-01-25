# vim: filetype=python ts=2 sw=2 sts=2 et :

import argparse
from random import random as r
import time
import math
import sys
import re

class o():
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return str(vars(i))


the = o(samples=64)

def tbl(rows=[]): return o(cols=[], rows=rows)
def col(txt='', pos=0): return o(n=0, txt=txt, pos=pos, has=None)
def order(): return o(all=[], sorted=False)

def ordered(order):
  if not order.sorted:
    order.all.sort()
  order.sorted = True
  return order.all

def symsp(x): return isinstance(x, dict)
def numsp(x): return isinstance(x, list)
def nump(x): return isinstance(x, (float, int))

def inc(col, x):
  col.n += 1
  if col.has is None:
    col.has = order() if nump(x) else {}
  has = col.has
  if symsp(has):
    has[x] = has.get(x, 0) + 1
  else:
    if len(has.all) < the.samples:
      has.all += [x]
      has.sorted = False
    elif r() < the.samples / col.n:
      has.all[int(r() * len(has.all))] = x
      has.sorted = False

def mu(ord): return sum(ord.all) / len(ord.all)

def norm(ord, x):
  a = ordered(ord)
  return (x - a[0]) / (a[-1] - a[0] + 1E-32)

def sd(ord):
  a = ordered(ord)
  return (a[int(.9 * len(a))] - a[int(.1 * len(a))]) / 2.56

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
  t.cols = [col(txt, n)
            for n, txt in enumerate(x) if not "?" in txt]

def body(t, x):
  [inc(c, x[c.pos]) for c in t.cols if x[c.pos] != "?"]
  t.rows += [x]

def table(src, t=None):
  t = t if t else tbl()
  for x in src:
    (body if t.cols else head)(t, x)
  return t


print(table(csv("../data/weather.csv")).cols[2])
