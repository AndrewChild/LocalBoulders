# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting anotated topos and maps. 

# TODO:
	Python:
	- gps coords for boulders
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
    LaTeX:
    - GPS index of boulders
    - arete shortcut
	- little bug where image links don't take you to the right page, but do display the right page
	- auto crop page and spread picture sizes
	- format photo captions to be on right side for even pages
	- add book options for index sections
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation