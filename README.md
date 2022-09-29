# LocalBoulders
 Framework for building bouldering guidebooks

# TODO:
	Python:
	- Add area maps feature
	- Intro?
	- gps coords for boulders
	- use of cammal case vs other conventions is inconsistent
	- PEP8?
	- is there a more elegant way to move through the data structure (e.g. reference grandchildren and grandparents in addition to parents and children, book.boulders or boulders.book)
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
	- remove metaclasses
    - use itertools.count for indexing
    - limit photo height
    - in contexts where both routes and variations are being refered to interchangably call them climbs
	- rework topo map drawing. If possible draw all sub area topos from the area map using layers
    LaTeX:
    - GPS index of boulders
    - arete shortcut
    - distribute photos (as in action shots, not topos and maps) evenly throughout an area instead of declaring them at the boulder level
	- minipages can overflow the bottom of a column
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation