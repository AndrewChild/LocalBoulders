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
    - limit photo height
	- seems like annotations are smaller in full width images
	- when assigning topos to boulders the code just assigns the topo to the first boulder declared in the routes attribute (not the first boulder in the book order). This is kind of useful but its not intended behaviour.
	- add support for YDS routes
	  - started this implementaion need to add new attributes to climb to track things link number of bolts routre height and pitches
	- histograms are small and hard to read. Might be good to group routes by color instead of V grade to save some space
    LaTeX:
    - GPS index of boulders
    - arete shortcut
    - distribute photos (as in action shots, not topos and maps) evenly throughout an area instead of declaring them at the boulder level?
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation
	- Action shots
		- places a action shot should pe able to be placed:
			full page or two page spread (p,s):
			- at the beginning/end of the document, area, or sub area
			full width (f):
			- before a formation item
			- at the end of a sub area
			- after an area or sub area description
			column (h):
			- before or after a route item