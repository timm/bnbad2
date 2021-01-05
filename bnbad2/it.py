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

from .boot import *

def help(): return [
    flag("show version", V=False),
    flag("data dir", data="/Users/timm/gits/timm/bnbad2/data"),
    # -------------------------------------
    flag("run one test", t=""),
    flag("run all tests", T=False),
    # -------------------------------------
    flag("char for 'less'", less="<"),
    flag("char for 'more'", more=">"),
    flag("char for 'skip'", skip="?"),
    flag("char for 'klass'", klass="!"),
    flag("char for symbols", sym="_"),
    flag("char for numerics", num=":"),
    # -------------------------------------
    flag("nb kludge for rare attributes", k=1),
    flag("nb kludge for rare classes", m=2),
    # -------------------------------------
    flag("contrast population", pop=20),
    flag("contrast generations", gen=20),
    flag("contrast trials", trials=50),
    # -------------------------------------
    flag("some epsilon", eps=.35),
    flag("some min", min=.5),
    flag("some want", want=128),
    # -------------------------------------
    flag("table samples", samples=64),
]

it = o(**{k: d for k, d, _ in help()})
