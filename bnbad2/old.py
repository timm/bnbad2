import sys
import random

def mu(a): return sum(a) / len(a)

def sd(a):
  n = len(a)
  lo, hi = .1 * n, .9 * n
  return (a[int(hi)] - a[int(lo)]) / 2.56


"""
T-test (parametric Significance Test)
Assuming the populations are bell-shaped curve, when are two curves not significantly different?
In their review of use of effect size in SE, Kampenses et al. report that many
papers use something like g >= 0.38 as the boundary between small effects and bigger effects.
See  equations 2,3,4 and Figure 9. or Systematic Review of Effect Size in
Software Engineering Experiments  Kampenes, Vigdis By, et al.
Information and Software Technology 49.11 (2007): 1073-1086.
"""
def same(i, j, conf=0.95, small=0.38, ordered=False):
  xs = [1, 2, 5, 10, 15, 20, 25, 30, 60, 100]
  ys = {0.9: [3.078, 1.886, 1.476, 1.372, 1.341,
              1.325, 1.316, 1.31, 1.296, 1.29],
        0.95: [6.314, 2.92, 2.015, 1.812, 1.753,
               1.725, 1.708, 1.697, 1.671, 1.66],
        0.99: [31.821, 6.965, 3.365, 2.764, 2.602,
               2.528, 2.485, 2.457, 2.39, 2.364]}
  if not ordered:
    i, j = sorted(i), sorted(j)
  ni, nj = len(i), len(j)
  mi, mj = mu(i), mu(j)
  si, sj = sd(i), sd(j)

  def hedges():
    num = (ni - 1) * si**2 + (nj - 1) * sj**2
    denom = (ni - 1) + (nj - 1)
    sp = (num / denom)**0.5
    delta = abs(mi - mj) / sp
    c = 1 - 3.0 / (4 * (ni + nj - 2) - 1)
    return delta * c < small

  def tTest():
    nom = abs(mi - mj)
    denom = ((si / ni + sj / nj)**0.5) if si + sj else 1
    df = min(ni - 1, nj - 1)
    cf = interpolate(df, xs, ys[conf])
    return cf >= nom / denom
  return tTest() or hedges()

def bchop(lst, x):
  lo, mid, hi = 0, 0, len(lst) - 1
  while lo <= hi:
    mid = (lo + hi) // 2
    if x < lst[mid]:
      hi = mid - 1
    elif x > mid:
      lo = mid + 1
    else:
      break
  return mid

def interpolate(x, xs, ys):
  if x <= xs[0]:
    return ys[0]
  elif x >= xs[-1]:
    return ys[-1]
  else:
    n = bchop(xs, x)
    y0, y1 = ys[n - 1], ys[n]
    x0, x1 = xs[n - 1], xs[n]
  return y0 + (x - x0) / (x1 - x0) * (y1 - y0)

# [0.147, 0.33, 0.474][1]):
def cliffs(lst1, lst2, m=20, dull=(.33 + .14) / 2):
  n1, n2 = len(lst1), len(lst2)
  n1 = 1 if n1 <= m else len(lst1) // m
  n2 = 1 if n2 <= m else len(lst2) // m
  n = gt = lt = 0.0
  for x in lst1[::n1]:
    for y in lst2[::n2]:
      n += 1
      if x > y:
        gt += 1
      if x < y:
        lt += 1
  return abs(lt - gt) / n <= dull

def ff1(n=10):
  def r(z): return round(z, 3)
  random.seed(1)
  a = sorted([random.random() for _ in range(n)])
  f = 1
  print("[f, ma, mb, sa, sb, d, same, cohen, cliffs]")
  while f < 3:
    b = sorted([f * x for x in a])
    d = sd(sorted(a + b)) * .35
    print([r(z) for z in [f, mu(a), mu(b), sd(a), sd(b), d]] + [
        1 if same(a, b) else 0,
        1 if abs(mu(a) - mu(b)) < d else 0,
        1 if cliffs(a, b) else 0])
    f = f * 1.07


ff1(10)
