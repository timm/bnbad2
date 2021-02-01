# INSTALL

###### curl -s https://raw.githubusercontent.com/timm/bnbad2/main/INSTALL.md > INSTALL.md)
###### run sh INSTALL.md

V=duo3  
git clone http://github.com/timm/bnbad2 bnbad2  
cd bndad2/bnbad2  
chmod +x $V.py  
./$V.py -h  


###### usage: duo3 [-h] [-best F] [-beam I] [-data S] [-path2data S] [-k I] [-m I]
######             [-seed I] [-lives I] [-rowsamples I] [-xsmall F] [-ysmall F]
######             [-Xchop F]
###### 
###### Optimizer, written as a data miner.  Break the data up into regions
###### of 'bad' and 'better'. 'Interesting' things occur at very different
###### frequencies in 'bad' and 'better'. Find interesting bits. Combine
###### them. Repeat. Nearly all this processing takes log linear time.
###### 
###### optional arguments:
######   -h, --help     show this help message and exit
######   -best F        [0.5]
######   -beam I        [10]
######   -data S        [auto93.csv]
######   -path2data S   [../data]
######   -k I           [1]
######   -m I           [2]
######   -seed I        [13]
######   -lives I       [128]
######   -rowsamples I  [64]
######   -xsmall F      [0.35]
######   -ysmall F      [0.35]
######   -Xchop F       [0.5]

