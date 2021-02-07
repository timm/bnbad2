class Obj:
  """After watching "stop writing classes",
   https://www.youtube.com/watch?v=o9pEzgHorH0, as an
   experiment, I replaced all my classes with
   structs. It was a successful experiment (code shrank by
   a factor of two). Still,  sometimes I want to customize 
   Python's magic methods. So..."""
  def __init__(i, **d): i.__dict__.update(**d)
  def __repr__(i): return i.__class__.__name__ + str(
      {k: v for k, v in sorted(i.__dict__.items()) if k[0] != "_"})

  @classmethod
  def kid(c, **d):
    for name, inits in d.items():
      globals()[name] = type(name, tuple([c]), inits)

def act(c):
  "Decorator magic: add method to class after it has been created"
  return lambda f: setattr(c, f.__name__,
                           lambda i, *l, **d: f(i, *l, **d))


# succinct way to defined a class
Obj.kid(Robot=dict(model=1970, n=2))

@ act(Robot)
def __lt__(i, j): return i.model < j.model


r = Robot(model=34) # can overrode defaults
print(r.model)
r.n = 49            # can set variables
print(r.n)          # let me show you
print(r)            # can print
print(r < Robot())  # can meta
