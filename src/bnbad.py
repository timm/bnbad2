# Find and combine interesting bits. Repeat.   
# [home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
# [cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html) 
# <hr>
# <a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
# [![DOI](https://zenodo.org/badge/318809834.svg)](https://zenodo.org/badge/latestdoi/318809834)  
# ![](https://img.shields.io/badge/platform-osx%20,%20linux-orange)    
# ![](https://img.shields.io/badge/language-python3,bash-blue)  
# ![](https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet)  
#  [![Build Status](https://travis-ci.com/timm/bnbad2.svg?branch=main)](https://travis-ci.com/timm/bnbad2)   
# ![](https://img.shields.io/badge/license-mit-lightgrey)
# --------

# Store csv data in a table. Summarize rows in columns.   
# Define column type and name in row1.   
# (C) 2021 Tim Menzies (timm@ieee.org) MIT License

from lib import Pretty
from it import it

#---------
# Super-class for columns.
class Col(Pretty):
  def __init__(i, pos=0,txt=""):
    i.pos, i.txt, i.n = pos,txt,0
    i.w  = -1 if it.ch.less in txt else 1
  # Add items, increment `n` (if not skipping `x`).
  def add(i,x): 
    if x != it.ch.skip:
      i.n += 1
      i.add1(x)
    return x
  # Return the number of bins
  def card(i):    return 0
  # Convert `x` to one of a small number of bins.
  def bin(i,x):   return x if x == it.ch.skip else i.bin1(i,x)
  # Normalize `x` to a fixed range
  def norm(i,x):  return x if x == it.ch.skip else i.norm1(i,x)
  # Default add: no nothing
  def add1(i,x):  pass
  # Default bin: just return `x`
  def bin1(i,x):  return x 
  # Default normalization: just return `x`
  def norm1(i,x): return x 

#-------
# For columns of symbols
class Sym(Pretty):
  def __init__(i,**d):
    super().__init__(**d) 
    i.seen = {}
    i.most, i.mode = 0,None
  def card(i):   return len(i.bins())
  def bins(i):   return i.seen.keys()
  # Track how many `x` we have seen.
  def add1(i,x):
    new = i.seen(x,0) + 1
    if new > i.most:
      i.most, i.mode = new, x

#-------
# For columns of numbers
class Some(Pretty):
  def __init__(i,s**d):
    super().__init__(**d) 
    i.ok=False 
    i.want=it.some.want
    i._cache, i._bins = [],[]
  # Cache up to `i.want` items, selected at random
  def add1(i,x) :
    r = random.random
    if i.n < i.want:
      i.ok= False
      i._cache += [x]
      i._bins=[]
    elif r() < i.want/i.n:
      i.ok= False
      i._cache[ int(r()*len(i._cache)) ] = x
      i._bins=[]
  # Return the cache, sorted.
  def all(i):
    i._cache = i._cache if i.ok else sorted(i._cache)
    i.ok = True
    return i._cache
  # Return the `p`-th percentile in the cache, bounded 
  # from `lo` to `hi`
  def per(i,p=.5, lo=0,hi=None):
    hi = hi or len(i._cache) 
    return i.all()[ int(lo + p*(hi-lo)) ]
  # Return the 50-th percentile in the cache, bounded 
  # from `lo` to `hi`
  def mid(i,**d): return i.per(p=.5, **d)
  # Return the standard deviation of cache values from lo to hi
  def sd(i,**d):  return (i.per(p=.9,**d) - i.per(p=.1,**d))/2.54
  # Normalize `x` to the range 0..1
  def norm1(i,x): return x 
    lst = i.all()
    lo,hi = lst[0], lst[-1]
    return (x - lo) / (hi - lo  + 1E-32)
  # Return the number of bins
  def card(i): return len(i.bins()) + 1    
  # Convert `x` to one of a small number of bins.
  def bin(i,x): 
    for n,y in enumerate(i.bins):
      if x<=y: return n
    return 1 + len(i.bins)
  # Return the bins.
  def bins(i):
    i._bins = i._bins or i.bins1(i)
    return i._bins
  def bins1(i,x): return pass
    
