# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting anotated topos and maps. 

# TODO:
	Python:
	- Intro?
	- gps coords for boulders
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
    - limit image height/add more functionality for image scalling
	- add full page and two page spread image sizes
	- add support for YDS routes
	  - started this implementaion need to add new attributes to climb to track things link number of bolts routre height and pitches
	- histograms are small and hard to read. Might be good to group routes by color instead of V grade to save some space
	- add list of photo creds to index
    LaTeX:
    - GPS index of boulders
	- Photo credit index
    - arete shortcut
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation