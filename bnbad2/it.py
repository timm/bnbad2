# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# [![DOI](https://zenodo.org/badge/326061406.svg)](https://zenodo.org/badge/latestdoi/326061406)<br>
# ![](https://img.shields.io/badge/platform-osx%20,%20linux-orange)<br>
# ![](https://img.shields.io/badge/language-python3,bash-blue)<br>
# ![](https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet)<br>
# [![Build Status](https://travis-ci.com/timm/bnbad2.svg?branch=main)](https://travis-ci.com/timm/bnbad2)<br>
# ![](https://img.shields.io/badge/license-mit-lightgrey)
# --------

from .boot import *

def help(): return [
    arg("char for less", less="<"),
    arg("char for more", more=">"),
    arg("char for skip", skip="?"),
    arg("char for klass", klass="!"),
    arg("char for symbols", sym="_"),
    arg("char for numerics", num=":"),
    arg("some epsilon", eps=.35),
    arg("some min", min=.5),
    arg("some want", want=128),
    arg("table samples", samples=64),
    arg("run demos", demos=False)
]

it = o(**{k: d for k, d, _ in help()})
