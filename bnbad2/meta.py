def _method(f): return lambda *l, **d: f(i, *l, **d)

class o:
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return str(
      {k: (v.__name__ + "()" if callable(v) else v)
       for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

def of(i, **methods):
  for k, f in methods.items():
    i.__dict__[k] = _method(f)
  return i

def Fred(a=2):
  def p(i): return i.a + i.c + 20
  def lt(i, j): return i.a < j.a
  return of(o(a=a, b=2, c=3), say=p, lt=lt)


f = Fred(a=-10000000000000000)
print(f.say())
print(f.lt(Fred()))
# f.say(100000000)
# g = Fred(10)
# print(g < f
