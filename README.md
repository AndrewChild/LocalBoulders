# LocalBoulders
 Local Boulders is a work in progress framework for building bouldering guidebooks. The framework provides a hierachical data structure for route information in a format which can easily be passed to formats such as tex or html using the JINJA2 templating engine. Local Boulders also performs several usful automatic function such as numbering and color coding climbs and formatting annotated topos and maps.
 
# Documentation
[Work in Progress Documentation](https://docs.google.com/document/d/1SdaC6Ra2RaYkczrwDnqLYQRvsJmOF2mg-aY8-hYBMIY/edit#heading=h.qtw326n5e7xy)
 
# Required Software
This project is being devloped on a 64 bit Windows environment, its highly likely that it will not run without modification on other systems. In addition to the following software several non native Python and LaTeX packages are used.
- Python 3.X
- Miktex
- inkscape
- Ghost script (optional, but highly recommended)

# TODO:
	Documentation:
	  - create gitHub project page
	Python:
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
	- topo doesn't work when using linked images in svgs and the input and output files are different (svg loses track of linked image)
	- there appears to be a bug in the histogram. Cliffs shows an that it has a 5.14 when it doesn't
    LaTeX:
    - GPS index of boulders
	- overhaul image captions
	  - dynamically set put command based on page size and text ammount
	  - If text doesn't use full box width change box size
    Other:
    - Consider alternatives to LaTeX. HTML?