# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting anotated topos and maps. 

# TODO:
	Python:
	- gps coords for boulders
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
	- histograms are small and hard to read. Might be good to group routes by color instead of V grade to save some space
    LaTeX:
    - GPS index of boulders
	- Photo credit index
    - arete shortcut
	- little bug where image links don't take you to the right page, but do display the right page
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation