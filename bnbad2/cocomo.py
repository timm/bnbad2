# vim: filetype=python ts=2 sw=2 sts=2 et :

import re
import pprint
import random
from copy import deepcopy as kopy

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

class o(Pretty):
  def __init__(i, **d): i.__dict__.update(**d)
  def __getitem__(i, k): return i.__dict__[k]
  def __setitem__(i, k, v): i.__dict__[k] = v

  def __iter__(i):
    for k in i.__dict__:
      yield k

# ```py


def cocomo(lo=dict(acap=):
  _ = 0
  ne = [[_, _, _, 1, 2, _], # bad if lohi
        [_, _, _, _, 1, _],
        [_, _, _, _, _, _],
        [_, _, _, _, _, _],
        [_, _, _, _, _, _],
        [_, _, _, _, _, _]]
  nw = [[2, 1, _, _, _, _], # bad if lolo
        [1, _, _, _, _, _],
        [_, _, _, _, _, _],
        [_, _, _, _, _, _],
        [_, _, _, _, _, _],
        [_, _, _, _, _, _]]
  nw4 = [[4, 2, 1, _, _, _], # very bad if  lolo
         [2, 1, _, _, _, _],
         [1, _, _, _, _, _],
         [_, _, _, _, _, _],
         [_, _, _, _, _, _],
         [_, _, _, _, _, _]]
  sw4 = [[_, _, _, _, _, _], # very bad if  hilo
         [_, _, _, _, _, _],
         [1, _, _, _, _, _],
         [2, 1, _, _, _, _],
         [4, 2, 1, _, _, _],
         [_, _, _, _, _, _]]
  # bounded by 1..6
  ne46 = [[_, _, _, 1, 2, 4], # very bad if lohi
          [_, _, _, _, 1, 2],
          [_, _, _, _, _, 1],
          [_, _, _, _, _, _],
          [_, _, _, _, _, _],
          [_, _, _, _, _, _]]
  sw = [[_, _, _, _, _, _], # bad if hilo
        [_, _, _, _, _, _],
        [_, _, _, _, _, _],
        [1, _, _, _, _, _],
        [2, 1, _, _, _, _]]
  sw26 = [[_, _, _, _, _, _], # bad if hilo
          [_, _, _, _, _, _],
          [_, _, _, _, _, _],
          [_, _, _, _, _, _],
          [1, _, _, _, _, _],
          [2, 1, _, _, _, _]]
  sw46 = [[_, _, _, _, _, _], # very bad if hilo
          [_, _, _, _, _, _],
          [_, _, _, _, _, _],
          [1, _, _, _, _, _],
          [2, 1, _, _, _, _],
          [4, 2, 1, _, _, _]]
  rules = dict(
      cplx=dict(acap=sw46, pcap=sw46, tool=sw46),  # 12
      ltex=dict(pcap=nw4),  # 4
      pmat=dict(acap=nw, pcap=sw46), # 6
      pvol=dict(plex=sw),  # 2
      rely=dict(acap=sw4, pcap=sw4, pmat=sw4), # 12
      ruse=dict(aexp=sw46, ltex=sw46),  # 8
      sced=dict(
          cplx=ne46, time=ne46, pcap=nw4, aexp=nw4, acap=nw4,
          plex=nw4, ltex=nw, pmat=nw, rely=ne, pvol=ne, tool=nw), # 34
      stor=dict(acap=sw46, pcap=sw46),  # 8
      team=dict(aexp=nw, sced=nw, site=nw),  # 6
      time=dict(acap=sw46, pcap=sw46, tool=sw26),  # 10
      tool=dict(acap=nw, pcap=nw, pmat=nw)) # 6

  # 10 20 [4 8 12 16 inf] [12 16]
  def from(lo, hi, bins, values):
    value = random.choice(values)
    for x in bins:
      if lo <= x <= value in bins:
        return lo, x
      lo=x
    return lo, hi

  # constraints= (bins, values)
  def grab1(lo, hi, constraints=None):
    if constraints:
      lo, hi=from(lo, hi, constraints[0], constraints[1])
    return random.uniform(lo, hi)

  def grab(name, f, lo, hi, constraints=None, cache=None, f=int, rules=None,):
    if cache:
      if not name in cache: cache[name] = f(
          grab1(lo, hi, constraints))
      return cache[name]
    return f(is1(lo, hi, bins))

  def F(name, lo, hi):
    return lambda b4, c; grab(name, lo, hi, constraints=c, cache=b4, f=float)
  def I(lo, hi):
    return lambda b4, c: grab(name, lo, hi, constraints=c, cache=b4, f=int)

  defaults = o(
      misc=o(kloc=F(2, 1000),
             a=F(2.2, 9.8),
             goal=F(0.1, 2)),
      pos=o(rely=I(1, 5), data=I(2, 5), cplx=I(1, 6),
            ruse=I(2, 6), docu=I(1, 5), time=I(3, 6),
            stor=I(3, 6), pvol=I(2, 5)),
      neg=o(acap=I(1, 5), pcap=I(1, 5), pcon=I(1, 5),
            aexp=I(1, 5), plex=I(1, 5), ltex=I(1, 5),
            tool=I(1, 5), site=I(1, 6), sced=I(1, 5)),
      sf=o(prec=I(1, 6), flex=I(1, 6), arch=I(1, 6),
           team=I(1, 6), pmat=I(1, 6)))
# ```
# This code initializes the parameters then overrides then with values
# in `listofdicts` (if any are supplied).
#
# ```py

  def __init__(i, listofdicts=[]):
    i.x, i.y, dd=o(), o(), kopy(Cocomo.defaults)
    # set up the defaults
    for d in dd:
      for k in dd[d]:
        i.x[k] = dd[d][k] # can't +=: no background info
    # apply any other constraints
    for dict1 in listofdicts:
      for k in dict1:
        try:
          i.x[k] += dict1[k] # now you can +=
        except Exception as e:
          print(k, e)
    # ----------------------------------------------------------
    for k in dd.misc:
      i.y[k] = i.x[k]()
    for k in dd.pos:
      i.y[k] = F(.073, .21)() * (i.x[k]() - 3) + 1
    for k in dd.neg:
      i.y[k] = F(-.178, -.078)() * (i.x[k]() - 3) + 1
    for k in dd.sf:
      i.y[k] = F(-1.56, -1.014)() * (i.x[k]() - 6)
    # ----------------------------------------------------------
# ```
# Effort model:
# ```py

  def effort(i):
    em, sf=1, 0
    b=(0.85 - 1.1) / (9.18 - 2.2) * i.x.a() + 1.1 + (1.1 - 0.8) * .5
    for k in Cocomo.defaults.sf:
      sf += i.y[k]
    for k in Cocomo.defaults.pos:
      em *= i.y[k]
    for k in Cocomo.defaults.neg:
      em *= i.y[k]
    return round(i.x.a() * em * (i.x.goal() * i.x.kloc()) ** (b + 0.01 * sf), 1)
# ```
# Risk model:
# ```py

  def risk(i, r=0):
    for k1, rules1 in rules.items():
      for k2, m in rules1.items():
        x = i.x[k1]()
        y = i.x[k2]()
        z = m[x - 1][y - 1]
        r += z
    return round(100 * r / 104, 1)


print(Cocomo([dict(team=I(2, 2))]))
