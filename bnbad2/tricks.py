# vim: filetype=python ts=2 sw=2 sts=2 et :

from typing import Dict, Any
import json
import hashlib
import time
import argparse
import random
import pprint
import math
import sys
import re
from itertools import combinations

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
