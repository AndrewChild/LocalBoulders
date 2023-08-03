# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting anotated topos and maps. 

# TODO:
	Python:
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
	- spread and full page formats should work for maps too
	- a lot of functions still reference name when they should reference item_id
	- need a way to flag photo objects to be included in non print version of book
    LaTeX:
    - GPS index of boulders
	- little bug where image links don't take you to the right page, but do display the right page
	- add book options for index sections
	- Expand area inclomplete function to just allow any kind of bolded warning to be added at the end of the description
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation