class Obj:
  """After watching "stop writing classes",
   https://www.youtube.com/watch?v=o9pEzgHorH0, as an
   experiment, I replaced all my classes with
   structs. It was a successful experiment (code shrank by
   a factor of two). Still,  sometimes I want to customize
   Python's magic methods. So..."""
  def __repr__(i): return i.__class__.__name__ + str(
      {k: v for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

  @classmethod
  def kid(c, **d):
    def maker(inits):
      def f(i, **kw):
        i.__dict__.update(**inits)
        i.__dict__.update(**kw)
      return f
    for name, inits in d.items():
      klass = globals()[name] = type(name, tuple([c]), {})
      setattr(klass, "__init__", maker(inits))

def method(c): return \
    lambda f: setattr(c, f.__name__, lambda i, *l, **d: f(i, *l, **d))


# succinct way to defined a class
Obj.kid(Robot=dict(model=1970, n=2, hi=100))

# add a method after creating a class.
@method(Robot)
def __lt__(i, j): return i.model < j.model


assert str(Robot()) == "Robot{'hi': 100, 'model': 1970, 'n': 2}"
r = Robot(model=34) # can override defaults
assert r.n == 2
r.n = 49            # can set variables
assert r.n == 49    # let me show you
assert str(r) == "Robot{'hi': 100, 'model': 34, 'n': 49}"
assert r < Robot()  # can meta
