
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

from .__init__ import *

import sys
cli = args(help, __doc__)
if cli.demos:
  print(cli)
