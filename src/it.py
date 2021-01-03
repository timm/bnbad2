# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# [![DOI](https://zenodo.org/badge/318809834.svg)](https://zenodo.org/badge/latestdoi/318809834)<br>
# ![](https://img.shields.io/badge/platform-osx%20,%20linux-orange)<br>
# ![](https://img.shields.io/badge/language-python3,bash-blue)<br>
# ![](https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet)<br>
#  [![Build Status](https://travis-ci.com/timm/bnbad2.svg?branch=main)](https://travis-ci.com/timm/bnbad2)<br>
# ![](https://img.shields.io/badge/license-mit-lightgrey)
# --------

from boot import *

it = items([
    item("magic characters defining column types",

         CH=[item("goals to be minimized", less="<"),
             item("goals to be maximized", more=">"),
             item("items to be skipped", skip="?"),
             item("define class columns", klass="!"),
             item("define symbolic column", sym="_"),
             item("define numeric column", num=":")
             ]),

    item("numeric column control",

         SOME=[item("epsilon", epsilon=.35),
               item("min", min=.5),
               item("want", want=128)
               ]),

    item("table control",

         TABLE=[item("number of stuff", samples=64)
                ])
])
