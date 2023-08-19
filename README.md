# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting annotated topos and maps. 

# TODO:
	Python:
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
    LaTeX:
    - GPS index of boulders
	- overhaul image captions
	  - dynamically set put command based on page size and text ammound
	  - If text doesn't use full box width change box size
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation