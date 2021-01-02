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

# Misc python routines. <br>
# (C) 2021 Tim Menzies timm@ieee.org MIT License

import pprint
import re
import random
import sys
from it import *

# ------------
# ## csv : read comma-separated file

# Iterate over each none empty line, killing
# whitespace and comments, splitting on commas.
def csv(file, sep=","):
  def prep(x):
    return float if it.CH.less in x or \
        it.CH.more in x or it.CH.num in x else str
  linesize = None
  with open(file) as fp:
    for n, line in enumerate(fp):
      line = re.sub(r'([\n\t\r ]|#.*)', '', line.strip())
      if line:
        line = line.split(sep)
        if linesize is None:
          linesize = len(line)
        assert len(line) == linesize,\
            "row size different to header size"
        if n == 0:
          cols = [prep(x) for x in line]
        else:
          line = [(x if x == it.CH.skip else f(x))
                  for f, x in zip(cols, line)]
        yield line

def csvok():
  all = [row for row in csv("data/weather.csv")]
  assert 15 == len(all)
  assert float == type(all[2][2])
  assert str == type(all[2][0])
  assert 399 == len([row for row in csv("data/auto93.csv")])


# ---
# main
if __name__ == "__main__":
  if "--test" in sys.argv:
    ok(csvok)
