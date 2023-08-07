# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting anotated topos and maps. 

# TODO:
	Python:
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
	- add option to rotate images
	  - should rotate full page insert image for print version and rotate page for pdf version
	  - maybe make new format 'pr' to support this
    LaTeX:
    - GPS index of boulders
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation