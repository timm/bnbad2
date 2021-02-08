class Obj:
  "For classes that are mostly data stores, with few (or no) methods."
  def __repr__(i): return i.__class__.__name__ + str(
      {k: v for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

def so(**d):
  name, *keys = list(d.keys())
  inits = {k: d[k] for k in keys}
  klass = globals()[name] = type(name, tuple([d[name]]), {})
  setattr(klass, "__init__",
          lambda i, **kw: i.__dict__.update({**inits, **kw}))

def of(c): return \
    lambda f: setattr(c, f.__name__, lambda i, *l, **d: f(i, *l, **d))


# succinct way to defined a class
so(Robot=Obj, model=1970, n=2, hi=100)

# add a method after creating a class.
@of(Robot)
def __lt__(i, j): return i.model < j.model


assert str(Robot()) == "Robot{'hi': 100, 'model': 1970, 'n': 2}"
r = Robot(model=34) # can override defaults
assert r.n == 2     # will build with local defaults
r.n = 49            # can set variables
assert r.n == 49    # let me show you
assert str(r) == "Robot{'hi': 100, 'model': 34, 'n': 49}"
assert r < Robot()  # can meta
print(r)
