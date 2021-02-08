class o:
  "For classes that are mostly data stores, with few (or no) methods."
  def __init__(i, **d): i.__dict__.update(d)
  def __repr__(i): return i.__class__.__name__ + str(
      {k: v for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

def _so(name, d, f):
  d, f = d.__dict__, f.__dict__
  k = globals()[name] = type(name, tuple([o]), {})
  setattr(k, "__init__",
          lambda i, ** kw: i.__dict__.update({**d, **kw}))
  [setattr(k, x, f[x]) for x in f]

def _do(c): return lambda f: setattr(c, f.__name__, lambda i,
                                     *l, **d: f(i, *l, **d))


if __name__ == "__main__":
  print(o(a=1, b=2))
  _so("Robot", o(model=1970, n=2, hi=100),
      o(__lt__=lambda i, j: i.model < j.model))
  # @_do(Robot)
  # def __lt__(i, j): return i.model < j.model
  assert str(Robot()) == "Robot{'hi': 100, 'model': 1970, 'n': 2}"
  r = Robot(model=34) # can override defaults
  assert r.n == 2     # will build with local defaults
  r.n = 49            # can set variables
  assert r.n == 49    # let me show you
  assert str(r) == "Robot{'hi': 100, 'model': 34, 'n': 49}"
  assert r < Robot()  # can meta
  print(r)
