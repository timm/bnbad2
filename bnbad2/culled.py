# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# <p><a href="https://zenodo.org/badge/latestdoi/326061406"><img src="https://zenodo.org/badge/326061406.svg"></a>
# <br><a href="https://badge.fury.io/py/bnbad2"><img src="https://badge.fury.io/py/bnbad2.svg" alt="PyPI version" height="18"></a>
# <br><img src="https://img.shields.io/badge/platform-osx%20,%20linux-orange">
# <br><img src="https://img.shields.io/badge/language-python3,bash-blue">
# <br><img src="https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet">
# <br><a href="https://travis-ci.com/timm/bnbad2"><img src="https://travis-ci.com/timm/bnbad2.svg?branch=main"></a>
# <br><img src="https://img.shields.io/badge/license-mit-lightgrey"></p><hr>

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
