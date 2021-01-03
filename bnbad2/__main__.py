
"""
Optimizer, written as a data miner.  Break the data up into regions
of 'bad' and 'better'. "Interesting' things occur at very different
frequencies in 'bad' and 'better'. Find interesting bits. Combine
them. Repeat. Nearly all this processing takes loglinear time.

     :-------:
     | Ba    | Bad <----.  planning= (better - bad)
     |    56 |          |  monitor = (bad - better)
     :-------:------:   |
             | B    |   v
             |    5 | Better
             :------:
"""

from .__init__ import *

import sys
cli = args(help, __doc__)
if cli.T:
  print(101)
