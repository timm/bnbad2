Non-parametric optimization.<br>
Find interesting bits. Combine them. Repeat.<br>
[home](http://menzies.us/bnbab2)         :: [lib](http://menzies.us/bnbad2/lib.html) ::
[cols](http://menzies.us/bnbad2/tab.html) :: [tbl](http://menzies.us/bnbad2/grow.html)<br>
<hr>
<a href="http://github.com/timm/bnbad2"><img src="https://github.com/timm/bnbad2/raw/main/etc/img/banner.png" align=left></a>
<p><a href="https://zenodo.org/badge/latestdoi/326061406"><img src="https://zenodo.org/badge/326061406.svg"></a>
<br><img src="https://img.shields.io/badge/language-python3,bash-blue">
<br><a href="https://badge.fury.io/py/bnbad2"><img src="https://badge.fury.io/py/bnbad2.svg" alt="PyPI version" height="18"></a>
<br><img src="https://img.shields.io/badge/purpose-ai%20,%20se-blueviolet">
<br><a href="https://travis-ci.com/timm/bnbad2"><img src="https://travis-ci.com/timm/bnbad2.svg?branch=main"></a>
<br><img src="https://img.shields.io/badge/license-mit-lightgrey"></p><hr>

# BnBad2

<a href="http://menzies.us/bnbad2"><pre>
                     _         _                  _                  
                    | |   _   | |                | |                 
  ____ ____ ____  _ | |  | |_ | | _   ____     _ | | ___   ____  ___ 
 / ___) _  ) _  |/ || |  |  _)| || \ / _  )   / || |/ _ \ / ___)/___)
| |  ( (/ ( ( | ( (_| |  | |__| | | ( (/ /   ( (_| | |_| ( (___|___ |
|_|   \____)_||_|\____|   \___)_| |_|\____)   \____|\___/ \____|___/ 
</pre></a>
                                                                     


```
usage: bnbad2 [-h] [-V] [-data S] [-t S] [-T] [-less S] [-more S] [-skip S]
              [-klass S] [-sym S] [-num S] [-k I] [-m I] [-pop I] [-gen I]
              [-trials I] [-eps F] [-min F] [-want I] [-samples I]
```

Optimizer, written as a data miner.  Break the data up into regions
of 'bad' and 'better'. 'Interesting' things occur at very different
frequencies in 'bad' and 'better'. Find interesting bits. Combine
them. Repeat. Nearly all this processing takes log linear time.

```            
:-------:              
| Ba    | Bad <----.       planning        = max(better - bad)
|    56 |          |       monitor         = max(bad - better)
:-------:------:   |       tabu            = min(bad + better)
        | B    |   v       active learning = find better == bad
        |    5 | Better
        :------:
```

Optional arguments:

```
-h, --help  show this help message and exit
-V          show version
-data S     data dir; e.g. -data /Users/timm/gits/timm/bnbad2/data
-t S        run one test
-T          run all tests
-less S     char for 'less'; e.g. -less <
-more S     char for 'more'; e.g. -more >
-skip S     char for 'skip'; e.g. -skip ?
-klass S    char for 'klass'; e.g. -klass !
-sym S      char for symbols; e.g. -sym _
-num S      char for numerics; e.g. -num :
-k I        nb kludge for rare attributes; e.g. -k 1
-m I        nb kludge for rare classes; e.g. -m 2
-pop I      contrast population; e.g. -pop 20
-gen I      contrast generations; e.g. -gen 20
-trials I   contrast trials; e.g. -trials 50
-eps F      some epsilon; e.g. -eps 0.35
-min F      some min; e.g. -min 0.5
-want I     some want; e.g. -want 128
-samples I  table samples; e.g. -samples 64
```
