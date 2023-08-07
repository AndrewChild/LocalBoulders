# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting anotated topos and maps. 

# TODO:
	Python:
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
	- spread and full page formats should work for maps too
	- reassess photo scales, half size is not actually 1/2 of the full size width (60mm vs 124mm)
    LaTeX:
    - GPS index of boulders
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation