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

# Install

Download file, `chmod +x file`, test using `./file.py -h`.

# License

(c) Tim Menzies, 2021
MIT License, https://opensource.org/licenses/MIT. The source code
does not need to be public when a distribution of the software is
made. Modifications to the software can be release under any
license. Changes made to the source code may not be documented.
"""

import argparse
from random import random as r
from random import seed as seed
from random import choice as choice
import time
import math
import sys
import re

class Obj():
  """Containers with set/get access, prints keys in sorted order
  ignoring 'private' keys (those starting with '_')."""
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return str(
      {k: v for k, v in sorted(i.__dict__.items()) if str(k)[0] != "_"})


the = Obj(
    best=0.5,
    data="auto93.csv",
    path2data="../data",
    rowsamples=64,
    xsmall=.35,
    ysmall=.35,
    Xchop=.5)

def table(src):
  """Converts a list of cells into rows, summarized in columns. Row1
  name describes each column. ':' and '_' and numbers and symbols (respectively)
  and '>' and '<' are goals to maximize or minimize (respectively). For example, in
  the following, we want to minimize weight (lbs) while maximizing acceleration (acc)
  and miles per gallon (mpg).

      _cylinders,:displ,:hp,<lbs,>acc,:model,_origin,>mpg

  For example, after reading weather.csv,
  then `.cols` would have entries like the following (and note that
  the first is for a symbolic column and the second is for a numeric):

      {'_outlook' :  {
              'has': # 'has' for symbolic is a dictionary
                     {'sunny': 5, 'overcast': 4, 'rainy': 5},
              'n'  : 14,
              'pos': 0,
              'txt': '_outlook',
               'w' : 1}
       '<temp'   :   {
              'has': # 'has' for  numerics is a list
                     [64, 85], # min and max value seen in this columnm
              'n'  : 14,
              'pos': 1,
              'txt': '<temp'}
      etc }

  Tables also collect rows with a 'score' (how often that row
  dominates 'rowsamples' other rows) and 'klass' which is often often
  that score is better than 'best'. e.g. if 'best'=0.5 then 'klass' is
  true if this row 'scores' better than half the others; e.g. from
  ../data/auto93.csv, here are the first and last four rows sorted by
  'score'. Observe that we want to minimize lbs and maximize acc and mpg.
  Hence, in the last rows, lbs is lower and acc and mpg is larger:

      score  klass  _cylin  :displ  :hp  <lbs  >acc  :model  _origin  >!mpg
      -----  ------ ------- ------- ---  ----  ----  ------  -------  -----
      0.0    False  8       400     175  5140  12    71      1        10
      0.0    False  8       440     215  4735  11    73      1        10
      0.0    False  8       454     220  4354  9     70      1        10
      0.0    False  8       455     225  4425  10    70      1        10
      0.0    False  8       455     225  4951  11    73      1        10
      -----  ------ ------- ------- ---  ----  ----  ------  -------  -----
      0.98   True   4       91      60   1800  16.4  78      3        40
      0.98   True   4       97      46   1835  20.5  70      2        30
      1.0    True   4       85      '?'  1835  17.3  80      2        40
      1.0    True   4       86      65   2110  17.9  80      3        50
      1.0    True   4       97      52   2130  24.6  82      2        40

  Also note that the 'klass' is 'True' for the better half and 'False'
  otherwise.

  """
  def Tbl(rows=[]): return Obj(cols={}, x={}, y={}, rows=rows)
  def Row(cells=[]): return Obj(cells=cells, score=0, klass=True)

  def Col(txt='', pos=0, w=1):
    return Obj(n=0, txt=txt, pos=pos, has=None, spans=[],
               w=-1 if "<" in txt else 1)

  def classify(tbl):
    def norm(lst, x): return (
        x - lst[0]) / (lst[1] - lst[0] + 1E-32)

    def better(tbl, row1, row2):
      "Zitler's continous domination predicate (from IBEA, 2005)."
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
                       for _ in range(the.rowsamples)) / the.rowsamples
    for n, row in enumerate(sorted(tbl.rows, key=lambda z: z.score)):
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
        col.has = [math.inf, -
                   math.inf] if isa(x, (float, int)) else {}
        return inc(col, x)
      col.n += 1
      if symsp(col.has):
        col.has[x] = col.has.get(x, 0) + 1
      else:
        if x > col.has[1]:
          col.has[1] = x
        if x < col.has[0]:
          col.has[0] = x
    [inc(c, x[c.pos]) for c in tbl.cols.values() if x[c.pos] != "?"]
    tbl.rows += [Row(x)]

  def footer(tbl):
    for col in tbl.cols.values():
      if numsp(col.has):
        col.has.sort()
    classify(tbl)
    discretize(tbl)
  ##########################
  tbl = Tbl()
  for x in src:
    (body if len(tbl.cols) else head)(tbl, x)
  footer(tbl)
  return tbl

def discretize(tbl):
  """Reports `bins` for each numeric columns. Initially,
  columns of `N` (x,y) values  into bins of size N^Xchop.
  Combines bins that are smaller than `sd(x)*xsmall`. Then combine
  bins that are different by less than `sd(y)*ysmall`. Also, if
  two adjacent bins are not not 'best', then they are dull and
  we fuse them.  For example, from ../data/auto93.csv, we
  get  learn that '-cylinders' effectively divides into 3:

    [{'hi': 4, 'lo': -inf},
     {'hi': 8, 'lo': 5},
     {'hi': inf, 'lo': 5}]

  Note that the above used 'best=.5' i.e.  we were were dividing data
  half:half into best:rest. But we ran the same code with 'best=.8' then
  we find a different picture of what is interesting or not:


    [{'hi': 4, 'lo': -inf},
     {'hi': inf, 'lo': 3}]

  That is, at 'best=.8' all we care about is whether or not 'cylinders'
  is above or below 3.;

  """

  def Span(lo=-math.inf, hi=math.inf, has=None):
    return Obj(lo=lo, hi=hi, _has=has if has else [])

  def mu(lst): return sum(lst) / len(lst)

  def sd(lst): return (
      lst[int(.9 * len(lst))] - lst[int(.1 * len(lst))]) / 2.56

  def pairs(lst, fx, fy):
    xs, ys, xy = [], [], []
    for one in lst:
      x = fx(one)
      if x != "?":
        y = fy(one)
        xs += [x]
        ys += [y]
        xy += [(x, y)]
    ys = sorted(ys)
    return (sd(sorted(xs)) * the.xsmall,
            sd(ys) * the.ysmall,
            ys[int(the.best * len(ys))],
            sorted(xy))

  def div(xsmall, ysmall, ymin, xy):
    n = len(xy)**the.Xchop
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
    out = merge(tmp, ymin, ysmall)
    out[0].lo = -math.inf
    out[-1].hi = math.inf
    return out

  def merge(b4, ymin, ysmall):
    j, now = 0, []
    while j < len(b4):
      a = b4[j]
      if j < len(b4) - 1:
        b = b4[j + 1]
        if (abs(mu(b._has) - mu(a._has)) < ysmall
            or
                (mu(b._has) < ymin and mu(a._has) < ymin)):
          merged = Span(lo=a.lo, hi=b.hi, has=a._has + b._has)
          now += [merged]
          j += 2
      now += [a]
      j += 1
    return merge(now, ymin, ysmall) if len(now) < len(b4) else now

  for col in tbl.x.values():
    if numsp(col.has):
      col.spans = div(*pairs(tbl.rows,
                             lambda z: z.cells[col.pos],
                             lambda z: z.score))
  return tbl

def counts(tbl):
  """Counts (class column attribute) inside `tbl`
   (where attributes are the discretized attributes).
   THe counts take the form: (ckass,attribute,range,col), count.
   For example, with best=.9, the counts from ../data/auto93.csv
   are as follows. Note the simplicity of the decision space:
   all that matters is displacement and horsepower is above below
   141 and 74

      (False, ':displacement', 141, 1) 154
      (False, ':displacement', inf, 1) 205
      (False, ':horsepower', 74, 2) 48
      (False, ':horsepower', inf, 2) 307
      ....
      (True, ':displacement', 141, 1) 38
      (True, ':displacement', inf, 1) 1
      (True, ':horsepower', 74, 2) 34
      (True, ':horsepower', inf, 2) 3
      ....

   """

  def Counts(): return Obj(f={}, h={})
  out = Counts()
  for row in tbl.rows:
    k = row.klass
    out.h[k] = out.h.get(k, 0) + 1
    for col in tbl.x.values():
      x = row.cells[col.pos]
      if x != "?":
        x = bin(col.spans, x) if numsp(col.has) else x
        v = (k, col.txt, x, col.pos)
        out.f[v] = out.f.get(v, 0) + 1
  return out

def bin(spans, x):
  "Misc: Maps numbers into a small number of bins."
  for span in spans:
    if span.lo <= x < span.hi:
      return span.hi
  return span.hi


def isa(x, y):
  "Returns true if `x` is of type `y`."
  return isinstance(x, y)

def numsp(x):
  "Returns true if `x` is a container for numbers."
  return isa(x, list)

def symsp(x):
  "Returns true if `x` is a container for symbols."
  return isa(x, dict)

def csv(file, sep=",", ignore=r'([\n\t\r ]|#.*)'):
  """Misc: reads csv files into list of strings.
  Kill whitespace and comments.
  Converts  strings to numbers, it needed. For example,
  the file ../data/weather.csv is turned into

    ['_outlook', '<temp', ':humid', '?wind', '?!play']
    ['sunny', 85, 85, 'FALSE', 'no']
    ['sunny', 80, 90, 'TRUE', 'no']
    ['overcast', 83, 86, 'FALSE', 'yes']
    ['rainy', 70, 96, 'FALSE', 'yes']
    etc

    """
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

def args(what, txt, d):
  """Misc: Converts a dictionary `d` of key=val
     into command line arguments."""
  def arg(txt, val):
    eg = "[%s]" % val
    if val is False:
      return dict(help=eg, action='store_true')
    return dict(help=eg, default=val,
                metavar=("I" if isa(val, int) else (
                    "F" if isa(val, float) else "S")),
                type=(int if isa(val, int) else (
                    float if isa(val, float) else str)))
  ###############
  p = argparse
  from argparse_color_formatter import ColorHelpFormatter
  parser = p.ArgumentParser(
      prog=what, description=txt,
      formatter_class=p.RawDescriptionHelpFormatter)
  for key, v in d.__dict__.items():
    parser.add_argument("-" + key, **arg(key, v))
  return Obj(**vars(parser.parse_args()))

def main(f):
  "Misc: called when used at top-level."
  tbl = discretize(table(csv(f)))
  c = counts(tbl)
  for k, v in c.f.items():
    print(k, v)


if __name__ == "__main__":
  the = args("duo3", __doc__, the)
  for k, v in counts(discretize(table(csv(the.path2data + "/" + the.data)))).f.items():
    print(k, v)
