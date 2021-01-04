
def src(x=None):
  def prep(z):
    z = z if type(z) is str else z.decode("utf-8")
    return z.strip()

  def bytedata():
    for y in x.decode("utf-8").splitlines():
      yield prep(y)

  def strings():
    for y in x.splitlines():
      yield prep(y)

  def csv():
    with open(x) as fp:
      for y in fp:
        yield prep(y)

  def stdin():
    for y in sys.stdin:
      yield prep(y)
  f = strings
  print("xx", x)
  if x is None:
    f = stdio
  elif type(x) is bytes:
    f = bytedata
  elif x[-4:] == ".csv":
    f = csv
  for y in f():
    yield y
