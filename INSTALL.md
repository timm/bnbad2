# INSTALL

## Minimal install (recommended for end users)

- Install python3.9
- Download [https://raw.githubusercontent.com/timm/bnbad2/main/bnbad2/duo3.py](https://raw.githubusercontent.com/timm/bnbad2/main/bnbad2/duo3.py)
- Download https://raw.githubusercontent.com/timm/bnbad2/main/data/auto93.csv

```
python3 duo3.py -path2data ./ -data auto93.csv -best .8
```

This should generate

```
NUM cylinders            : [4, inf]
NUM displacement         : [104, 181, inf]
NUM horsepower           : [74, inf]
NUM model                : [72, inf]
NUM origin               : [3, inf]

True
  N, <lbs, >acc, >mpg
  71, 1987.61, 17.76, 33.38	displacement = (104) and horsepower = (74)
  88, 2119.48, 17.77, 32.16	horsepower = (74)
  99, 2045.59, 17.09, 32.02	displacement = (104)

False
  N, <lbs, >acc, >mpg
  316, 3198.52, 14.99, 21.58	horsepower = (inf)
  316, 3198.52, 14.99, 21.58	cylinders = (4 or inf) and horsepower = (inf)
  312, 3208.77, 15.01, 21.60	cylinders = (inf) and horsepower = (inf)
  394, 2976.23, 15.59, 23.88	cylinders = (inf)
  274, 3313.38, 14.98, 20.84	horsepower = (inf) and origin = (3)
  274, 3313.38, 14.98, 20.84	cylinders = (4 or inf) and horsepower = (inf) and origin = (3)
  319, 3155.96, 15.42, 22.29	origin = (3)
  274, 3313.38, 14.98, 20.84	cylinders = (inf) and horsepower = (inf) and origin = (3)
  319, 3155.96, 15.42, 22.29	cylinders = (inf) and origin = (3)
  266, 3167.44, 15.31, 22.11	cylinders = (4 or inf) and horsepower = (inf) and model = (inf)
```

### Full install (recommended for developers)

This installs the entire dev environment used to make this tool.


- First, install python3.9 and pip3.
- Second, download the repo

```
git clone http://github.com/timm/bnbad2 bnbad2  
cd bndad2
sudo pip3 install -r requirements.txt
cd bndad2
chmod +x duo3.py  
./duo3.py -h  
```

This should generate something like:

```
usage: duo3 [-h] [-best F] [-beam I] [-data S] [-path2data S] [-k I] [-m I]
            [-seed I] [-lives I] [-rowsamples I] [-xsmall F] [-ysmall F]
            [-Xchop F]

Optimizer, written as a data miner.  Break the data up into regions
of 'bad' and 'better'. 'Interesting' things occur at very different
frequencies in 'bad' and 'better'. Find interesting bits. Combine
them. Repeat. Nearly all this processing takes log linear time.

optional arguments:
  -h, --help     show this help message and exit
  -best F        [0.5]
  -beam I        [10]
  -data S        [auto93.csv]
  -path2data S   [../data]
  -k I           [1]
  -m I           [2]
  -seed I        [13]
  -lives I       [128]
  -rowsamples I  [64]
  -xsmall F      [0.35]
  -ysmall F      [0.35]
  -Xchop F       [0.5]
```

Next, try

```
./duo3.py -best .8 -data auto93.csv
```

This should generate the same as seen above (in the minimum install).

