"""
Local Boulders Guidebook builder v0.6
"""
import sys
import os.path
from datetime import datetime
from collections import OrderedDict
from genLaTeX import gen_book_LaTeX
from lbResources import genHistogram
from dataStructure.base_classes.LBItem import LBItem
from dataclasses import dataclass, field
from typing import Dict, List, Any, ClassVar


@dataclass(kw_only=True)
class Book(LBItem):
    repo: str
    dl: str
    collaborators: List[str]
    file_name: str = 'guidebook'
    options: Dict[str, Any] = field(default_factory=dict)

    __class_id: ClassVar[str] = 'books'
    ref: ClassVar[str] = 'bk'
    class_name: ClassVar[str] = 'book'
    __path_defaults: ClassVar[Dict[str, Any]] = {
        'graphics': './maps', #this is just a dummy that ensures that the maps folder is created
        'histogram_o': './maps/plots/',
        'qr_o': './maps/qr/',
        'topo_i': './maps/topos/',
        'topo_o': './maps/topos/',
        'subarea_i': './maps/area/',
        'subarea_o': './maps/area/out/',
        'area_i': './maps/area/',
        'area_o': './maps/area/out/',
        'photos': './images/'
    }
    __option_defaults: ClassVar[List[str]] = {
        'subarea_numbering': True,
        # if yes route numbering resets at zero for each sub area, if no it restarts for each area
        'use_ghost_script': True,
        # if yes the pdf will be compressed using ghost script
        'paper size': 'A5bld',
        # controls cropping of p (page) and s (spread) action photos A5bld is A5 with bleed region
    }

    def __post_init__(self):
        super().__post_init__()
        self.paths = {**self.__path_defaults, **self.paths}
        self.options = {**self.__option_defaults, **self.options}

        self.book = self
        self.areas = OrderedDict()
        self.subareas = OrderedDict()
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()
        self.climbs = OrderedDict()  # container for routes and variations
        self.all_photos = []  # container for all action and scenery photos in book
        self.all_maps = []  # container for all layout maps and topos in book

        self.date = datetime.today().strftime('%Y-%m-%d')
        self.area_colors = ['BrickRed', 'RoyalPurple', 'BurntOrange', 'Aquamarine', 'RubineRed', 'PineGreen', 'Bittersweet']
        self.area_colors_hex = ['#CB4154', '#7851A9', '#CC5500', '#00B5BD', '#E0115F', '#01796F', '#C04F17']
        self.color_scales = {
            'colors': ['black', 'green', 'RoyalBlue', 'DarkGoldenrod', 'DarkRed'],
            'Hueco': [-2, 3.6, 6.6, 9.6],
            'YDS': [-1, 10, 12, 14],
        }

    def gen(self):
        gen_book_LaTeX(self)

    def _init_paths(self):
        """
        ensures that all paths in os.paths exist
        """
        for path in self.paths.values():
            if not os.path.exists(path):
                print(f'Creating new directory: {path}')
                os.makedirs(path)

    def update(self):
        self._init_paths()
        if self.dl:
            self.create_qr(self.paths['qr_o'], self.dl, f'{self.item_id}')
        for area in self.areas.values():
            area.update()
        for map_item in self.all_maps:
            map_item.update()
        genHistogram(self)


if __name__ == '__main__':
    sys.exit()
