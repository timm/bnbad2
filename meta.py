import types
class Box:
  "For classes that are mostly data stores, with few (or no) methods."
  def __repr__(i): return i.__class__.__name__ + str(
      {k: v for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

def _so(**d):
  def funp(x): return isinstance(x, types.FunctionType)
  name, *keys = list(d.keys())
  data = {k: d[k] for k in keys if not funp(d[k])}
  klass = globals()[name] = type(name, tuple([d[name]]), {})
  setattr(klass, "__init__",
          lambda i, **kw: i.__dict__.update({**data, **kw}))
  for k in d:
    if funp(d[k]):
      setattr(klass, k, d[k])

def _do(c): return lambda f: setattr(c, f.__name__, lambda i,
                                     *l, **d: f(i, *l, **d))


if __name__ == "__main__":
  _so(Robot=Box, model=1970, n=2, hi=100,
      __lt__=lambda i, j: i.model < j.model)
  # @_do(Robot)
  #def __lt__(i, j): return i.model < j.model
  assert str(Robot()) == "Robot{'hi': 100, 'model': 1970, 'n': 2}"
  r = Robot(model=34) # can override defaults
  assert r.n == 2     # will build with local defaults
  r.n = 49            # can set variables
  assert r.n == 49    # let me show you
  assert str(r) == "Robot{'hi': 100, 'model': 34, 'n': 49}"
  assert r < Robot()  # can meta
  print(r)
