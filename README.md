# LocalBoulders
 Framework for building bouldering guidebooks

# TODO:
	Python:
	- Add area maps feature
	- Intro?
	- gps coords for boulders
	- use of cammal case vs other conventions is inconsistent
	- PEP8?
	- is there a more elegant way to move through the data stucrue (e.g. reference grandchildren and grandparents in addition to parents and children, book.boulders or boulders.book)
	- move LaTeX specific stuff to its own folder/project
        - maybe move class.ref to genLaTeX
	- remove metaclasses
    - use itertools.count for indexing
    - instead of assigning topos to boulders assign them to their lowest numbered route?
    - limit photo height
    - in contexts where both routes and variations are being refered to interchangably call them climbs
	- resize topo annotations (30% bigger)
		- calculate width of text string in label and resize label border perfectly
    LaTeX:
    - GPS index of boulders
    - arete shortcut
	- increase font size?
    - support half and full page photo sizes
    - there seems to be no way to include a full page photo on the first page of a chapter
    - distribute photos (as in action shots, not topos and maps) evenly throughout an area instead of declaring them at the boulder level
	- fix index columns
    Other:
    - Consider alternatives to LaTeX. HTML?
    - documentation