# Non-parametric optimization.<br>
# Find interesting bits. Combine them. Repeat.<br>
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# <p><a href="https://zenodo.org/badge/latestdoi/326061406"><img src="https://zenodo.org/badge/326061406.svg"></a>
# <br><img src="https://img.shields.io/badge/platform-osx%20,%20linux-orange">
# <br><img src="https://img.shields.io/badge/language-python3,bash-blue">
# <br><img src="https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet">
# <br><a href="https://travis-ci.com/timm/bnbad2"><img src="https://travis-ci.com/timm/bnbad2.svg?branch=main"></a>
# <br><img src="https://img.shields.io/badge/license-mit-lightgrey"></p><hr>

"""
Optimizer, written as a data miner.  Break the data up into regions
of 'bad' and 'better'. "Interesting' things occur at very different
frequencies in 'bad' and 'better'. Find interesting bits. Combine
them. Repeat. Nearly all this processing takes loglinear time.

  :-------:              
  | Ba    | Bad <----.       planning        = max(better - bad)
  |    56 |          |       monitor         = max(bad - better)
  :-------:------:   |       tabu            = min(bad + better)
          | B    |   v       active learning = find better == bad
          |    5 | Better
          :------:
"""

import sys
import pkg_resources
from .__init__ import *


cli = args(help, __doc__)
if cli.demos:
  print(data("weather.csv"))
  # for y in src(data("weather.csv")): for z in y.split(","): print(z.strip())
  # print(cli)
