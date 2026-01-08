"""
Local Boulders Guidebook builder v0.6
"""
import sys
from PIL import Image
from topo import update_svg
from lbResources import get_grade_atts, create_qr, mod_file_extension
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class Item:
    """
    Base class for all items in the book hierarchy (book, area, subarea, etc.)
    """
    name: str
    options: Dict[str, Any] = field(default_factory=dict, kw_only=True)
    paths: Dict[str, Any] = field(default_factory=dict, kw_only=True)
    format_options: List[str] = field(default_factory=list, kw_only=True)
    description: str = field(default='', kw_only=True)
    gps: str = field(default='', kw_only=True)
    parent: object = field(default=None, kw_only=True)
    item_id: str = field(default=None, kw_only=True)
    note: str = field(default=None, kw_only=True)

    def __post_init__(self):
        self.photos = []  # container for all action and scenery photos attached to an item
        self.maps = []  # container for all layout maps and topos attached to an item
        self.images = []  # container for all images attached to item

        if not self.item_id:
            self.item_id = self.name
        if not self.paths:
            self.paths = self.parent.paths
        else:
            if self.parent:
                self.paths = {**self.parent.paths, **self.paths}
        if not self.options and self.parent:
            self.options = self.parent.options

        if self.gps:
            self.gps = self.gps.replace(' ', '')
            create_qr(self.paths['qr_o'], 'http://maps.google.com/maps?q=' + self.gps, f'{self.item_id}')

    def assign_to_dic(self, container, connection):
        if connection.item_id in getattr(self, container):
            raise AttributeError(f'Item id "{connection.item_id}" is not unique')
        getattr(self, container).update({connection.item_id: connection})


@dataclass
class Climb(Item):
    """
    Base class for all items that contain route information (e.g. boulder problem, rope route, boulder variation)
    """
    grade: str = '?'
    description: str = "PLACEHOLDER"
    rating: int = -1
    serious: int = 0
    grade_unconfirmed: bool = False
    name_unconfirmed: bool = False
    FA: str = None

    def __post_init__(self):
        super().__post_init__()
        self.color, self.color_hex, self.gradeNum, self.grade_scale, self.grade_str = get_grade_atts(self.grade)
        self.hasTopo = False


@dataclass
class ItemImage(Item):
    """
    Base class for all image items (photos, topos, and maps. Inherits from item)
    """
    file_name: str
    size: str = field(default='h', kw_only=True)
    loc: str = field(default='b', kw_only=True)

    def __post_init__(self):
        super().__post_init__()
        self.out_file_name = self.file_name
        self.path = self.paths['photos']
        self.path_o = self.path
        self.book = self.parent.book
        self.parent.images.append(self)
        self.aspect_ratio = None
        page_aspects = {  # holds aspect ratios of various paper sizes. currently only A5 is supported
            'A5': 148 / 210
        }
        if self.size == 'p':
            self.aspect_ratio = page_aspects[self.book.options['paper size']]
        elif self.size in ['s', 'pr']:
            self.aspect_ratio = 1/page_aspects[self.book.options['paper size']]

    def save_insert(self):
        im = Image.open(self.path_o + self.out_file_name).convert('RGB')
        self.out_file_name = mod_file_extension(self.file_name, '.pdf')
        w_i, h_i = im.size
        aspect_ratio_i = w_i / h_i
        if aspect_ratio_i < self.aspect_ratio:
            h = w_i / self.aspect_ratio
            h_adj = (h_i - h) / 2
            im = im.crop((0, 0 + h_adj, w_i, h_i - h_adj))
        else:
            w = h_i * self.aspect_ratio
            w_adj = (w_i - w) / 2
            im = im.crop((0 + w_adj, 0, w_i - w_adj, h_i))

        if self.size == 's':
            w, h = im.size
            im1 = im.crop((0, 0, w / 2, h))
            im2 = im.crop((w / 2, 0, w, h))
            im1.save(self.path_o + self.out_file_name, 'PDF', resolution=100.0, save_all=True, append_images=[im2])
        else:
            im.save(self.path_o + self.out_file_name, 'PDF', resolution=100.0, save_all=True)


@dataclass
class ItemMap(ItemImage):
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
