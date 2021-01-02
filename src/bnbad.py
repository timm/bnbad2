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
  def add(i,x): 
    if x != it.ch.skip:
      i.n += 1
      i.add1(x)
    return x
  def bin(i,x):   return x if x == it.ch.skip else i.bin1(i,x)
  def norm(i,x):  return x if x == it.ch.skip else i.norm1(i,x)
  def add1(i,x):  pass
  def bin1(i,x):  return x 
  def norm1(i,x): return x 
  def card(i):    return 0

#-------
# For columns of symbols
class Sym(Pretty):
  def __init__(i,*l):
    super().__init__(*l) 
    i.seen = {}
    i.most, i.mode = 0,None
  def card(i):   return len(i.bins())
  def bins(i):   return i.seen.keys()
  def add1(i,x):
    new = i.seen(x,0) + 1
    if new > i.most:
      i.most, i.mode = new, x

#-------
# For columns of numbers
class Some(Pretty):
  def __init__(i,*l):
    super().__init__(*l) 
    i.ok=False 
    i.want=it.some.want
    i._all, i._bins = [],[]
  def add1(i,x) :
    r=random.random
    if i.n < i.want:
      i._all += [x]
      i.ok= False
    elif r() < i.want/i.n:
      i._all[ int(r()*len(i._all)) ] = x
      i.ok= False
  def all(i):
    i._all = i._all if i.ok else sorted(i._all)
    i.ok = True
    return i._all
      

  def card(i): return len(i.bins()) + 1    
  def bin(i,x): 
    for n,y in enumerate(i.bins):
      if x<=y: return n
    return 1 + len(i.bins)
  def bins(i):
    i._bins = i._bins or i.bins1(i)
    return i._bins
  def bins1(i,x): return pass
    
