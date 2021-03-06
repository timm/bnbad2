Module duo3
===========
Optimizer, written as a data miner.  Break the data up into regions
of 'bad' and 'better'. 'Interesting' things occur at very different
frequencies in 'bad' and 'better'. Find interesting bits. Combine
them. Repeat. Nearly all this processing takes log linear time.

     :-------:                 explore  = better==bad
     | Ba    | Bad <----.      planning = max(better - bad)
     |    56 |          |      monitor  = max(bad - better)
     :-------:------:   |      tabu     = min(bad + better)
             | B    |   v
             |    5 | Better
             :------:

# Install

Download file, `chmod +x file`, test using `./file.py -h`.

# License

(c) Tim Menzies, 2021
MIT License, https://opensource.org/licenses/MIT. The source code
does not need to be public when a distribution of the software is
made. Modifications to the software can be release under any
license. Changes made to the source code may not be documented.

Functions
---------

    
`args(what, txt, d)`
:   Misc: Converts a dictionary `d` of key=val
    into command line arguments.

    
`bin(spans, x)`
:   Misc: Maps numbers into a small number of bins.

    
`counts(tbl)`
:   Counts (class column attribute) inside `tbl`
    (where attributes are the discretized attributes).
    THe counts take the form: (ckass,attribute,range,col), count.
    For example, with best=.9, the counts from ../data/auto93.csv
    are as follows. Note the simplicity of the decision space:
    all that matters is displacement and horsepower is above below
    141 and 74
    
       (False, ':displacement', 141, 1) 154
       (False, ':displacement', inf, 1) 205
       (False, ':horsepower', 74, 2) 48
       (False, ':horsepower', inf, 2) 307
       ....
       (True, ':displacement', 141, 1) 38
       (True, ':displacement', inf, 1) 1
       (True, ':horsepower', 74, 2) 34
       (True, ':horsepower', inf, 2) 3
       ....

    
`csv(file, sep=',', ignore='([\\n\\t\\r ]|#.*)')`
:   Misc: reads csv files into list of strings.
    Kill whitespace and comments.
    Converts  strings to numbers, it needed. For example,
    the file ../data/weather.csv is turned into
    
      ['_outlook', '<temp', ':humid', '?wind', '?!play']
      ['sunny', 85, 85, 'FALSE', 'no']
      ['sunny', 80, 90, 'TRUE', 'no']
      ['overcast', 83, 86, 'FALSE', 'yes']
      ['rainy', 70, 96, 'FALSE', 'yes']
      etc

    
`discretize(tbl)`
:   Reports `bins` for each numeric columns. Initially,
    columns of `N` (x,y) values  into bins of size N^Xchop.
    Combines bins that are smaller than `sd(x)*xsmall`. Then combine
    bins that are different by less than `sd(y)*ysmall`. Also, if
    two adjacent bins are not not 'best', then they are dull and
    we fuse them.  For example, from ../data/auto93.csv, we
    get  learn that '-cylinders' effectively divides into 3:
    
      [{'hi': 4, 'lo': -inf},
       {'hi': 8, 'lo': 5},
       {'hi': inf, 'lo': 5}]
    
    Note that the above used 'best=.5' i.e.  we were were dividing data
    half:half into best:rest. But we ran the same code with 'best=.8' then
    we find a different picture of what is interesting or not:
    
    
      [{'hi': 4, 'lo': -inf},
       {'hi': inf, 'lo': 3}]
    
    That is, at 'best=.8' all we care about is whether or not 'cylinders'
    is above or below 3.;

    
`isa(x, y)`
:   Returns true if `x` is of type `y`.

    
`main(f)`
:   Misc: called when used at top-level.

    
`numsp(x)`
:   Returns true if `x` is a container for numbers.

    
`r()`
:   random() -> x in the interval [0, 1).

    
`symsp(x)`
:   Returns true if `x` is a container for symbols.

    
`table(src)`
:   Converts a list of cells into rows, summarized in columns. Row1
    name describes each column. ':' and '_' and numbers and symbols (respectively)
    and '>' and '<' are goals to maximize or minimize (respectively). For example, in
    the following, we want to minimize weight (lbs) while maximizing acceleration (acc)
    and miles per gallon (mpg).
    
        _cylinders,:displ,:hp,<lbs,>acc,:model,_origin,>mpg
    
    For example, after reading weather.csv,
    then `.cols` would have entries like the following (and note that
    the first is for a symbolic column and the second is for a numeric):
    
        {'_outlook' :  {
                'has': # 'has' for symbolic is a dictionary
                       {'sunny': 5, 'overcast': 4, 'rainy': 5},
                'n'  : 14,
                'pos': 0,
                'txt': '_outlook',
                 'w' : 1}
         '<temp'   :   {
                'has': # 'has' for  numerics is a list
                       [64, 85], # min and max value seen in this columnm
                'n'  : 14,
                'pos': 1,
                'txt': '<temp'}
        etc }
    
    Tables also collect rows with a 'score' (how often that row
    dominates 'rowsamples' other rows) and 'klass' which is often often
    that score is better than 'best'. e.g. if 'best'=0.5 then 'klass' is
    true if this row 'scores' better than half the others; e.g. from
    ../data/auto93.csv, here are the first and last four rows sorted by
    'score'. Observe that we want to minimize lbs and maximize acc and mpg.
    Hence, in the last rows, lbs is lower and acc and mpg is larger:
    
        score  klass  _cylin  :displ  :hp  <lbs  >acc  :model  _origin  >!mpg
        -----  ------ ------- ------- ---  ----  ----  ------  -------  -----
        0.0    False  8       400     175  5140  12    71      1        10
        0.0    False  8       440     215  4735  11    73      1        10
        0.0    False  8       454     220  4354  9     70      1        10
        0.0    False  8       455     225  4425  10    70      1        10
        0.0    False  8       455     225  4951  11    73      1        10
        -----  ------ ------- ------- ---  ----  ----  ------  -------  -----
        0.98   True   4       91      60   1800  16.4  78      3        40
        0.98   True   4       97      46   1835  20.5  70      2        30
        1.0    True   4       85      '?'  1835  17.3  80      2        40
        1.0    True   4       86      65   2110  17.9  80      3        50
        1.0    True   4       97      52   2130  24.6  82      2        40
    
    Also note that the 'klass' is 'True' for the better half and 'False'
    otherwise.

Classes
-------

`Obj(**d)`
:   Containers with set/get access, prints keys in sorted order
    ignoring 'private' keys (those starting with '_').