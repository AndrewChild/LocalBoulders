# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting anotated topos and maps. 

# TODO:
	Python:
	- Intro?
	- gps coords for boulders
	- use of cammal case vs other conventions is inconsistent
	- PEP8?
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
    - use itertools.count for indexing?
    - limit photo height
	- seems like annotations are smaller in full width images
    - in contexts where both routes and variations are being refered to interchangably call them climbs
	- when assigning topos to boulders the code just assigns the topo to the first boulder declared in the routes attribute (not the first boulder in the book order). This is kind of useful but its not intended behaviour.
	- add support for YDS routes
	  - started this implementaion need to add new attributes to climb to track things link number of bolts routre height and pitches
	  - right now the grades go into the same histogram should probably change or expand that
    LaTeX:
    - GPS index of boulders
    - arete shortcut
    - distribute photos (as in action shots, not topos and maps) evenly throughout an area instead of declaring them at the boulder level
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation