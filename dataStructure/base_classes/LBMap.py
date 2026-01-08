"""
Local Boulders Guidebook builder v0.6
"""
import sys
from update_svg import update_svg
from dataStructure.base_classes.LBImage import LBImage
from lbResources import mod_file_extension
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class LBMap(LBImage):
    """
    Base class for annotated map images (topos and maps)
    """
    file_name: str
    routes: List[object] = field(default_factory=list)
    sub_areas: Dict[str, Any] = field(default_factory=dict)
    out_file_name: str = field(default=None, kw_only=True)
    layers: List[str] = field(default_factory=list, kw_only=True)
    border: str = field(default=None, kw_only=True)

    def __post_init__(self):
        out_file_name = self.out_file_name
        super().__post_init__()
        self.out_file_name = out_file_name # hacky workaround to prevent ItemImage from overwriting this
        self.routes = self.routes.copy()  # not sure if this is necessary

        self.book.all_maps.append(self)
        self.parent.maps.append(self)

        self.path_o = self.paths[f'{self.path_id}_o']
        self.path_i = self.paths[f'{self.path_id}_i']

        if not self.out_file_name:
            if self.size in ['p', 'pr', 's']:
                self.out_file_name = mod_file_extension(self.file_name, '_c.pdf')
            else:
                self.out_file_name = mod_file_extension(self.file_name, '_c.png')

        photo_scales = {  # this is the amount that annotations should be scaled by for each photo size. This is
            # currently hard coded for the LaTeX template
            'h': 124 / 60,  # half page width
            'f': 124 / 124,  # full page width
            'p': 124 / 148,  # page width (i.e. photo page insert)
            'pr': 124 / 210,  # page width (i.e. photo page insert)
            's': 124 / (148 * 2),  # 2-page spread
        }
        self.scale = photo_scales[self.size]

    def update(self):
        update_svg(self)


if __name__ == '__main__':
    sys.exit()
