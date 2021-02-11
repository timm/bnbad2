import types
import copy

def fun(x): return isinstance(x, types.FunctionType)

class o:
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return str(
      {k: (v.__name__ + "()" if fun(v) else v)
       for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

def so(**d):
  i = o()
  i.__dict__ = {k: ((lambda *l, **kw: v(i, *l, **kw)) if fun(v) else v)
                for k, v in d.items()}
  return i

def Fred(a=2):
  def p(i, n=100): print(str(i.a + i.c + n))
  return so(a=a, b=2, c=3, say=p)


f = Fred(a=-10000000000000000)
f.say(100000000)
