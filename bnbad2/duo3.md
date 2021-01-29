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

## Install

Download file, `chmod +x file`, test using `./file.py -h`.

## License

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
:   Counts (class column attribute).

    
`csv(file, sep=',', ignore='([\\n\\t\\r ]|#.*)')`
:   Misc: reads csv files into list of strings.
    Kill whitespace and comments. 
    Converts  strings to numbers, it needed.

    
`discretize(tbl)`
:   Reports `bins` for each numeric columns. Initially,
    columns of `N` (x,y) values  into bins of size N^Xchop.
    Combines bins that are smaller than `sd(x)*xsmall`. Then combine
    bins that are different by less than `sd(y)*ysmall`.

    
`isa(x, y)`
:   

    
`main(f)`
:   Misc: called when used at top-level.

    
`numsp(x)`
:   

    
`r()`
:   random() -> x in the interval [0, 1).

    
`symsp(x)`
:   

    
`table(src)`
:   Converts a list of cells into rows, summarized in columns.
    Columns have `weights' which are positive/negative for things
    we want to minimize, maximize. Rows are scored according to how many
    other rows they dominate.

Classes
-------

`Obj(**d)`
:   Containers with set/get access, prints keys in sorted order
    ignoring 'private' keys (those starting with '_').
