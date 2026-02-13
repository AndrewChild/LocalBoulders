"""
Local Boulders Guidebook builder v0.6
"""
import sys
from PIL import Image
from dataStructure.base_classes.LBItem import LBItem
from lbResources import mod_file_extension
from dataclasses import dataclass, field


@dataclass
class LBImage(LBItem):
    """
    Base class for all image items (photos, topos, and maps. Inherits from item)
    """
    file_name: str
    width: float = field(default=0.9, kw_only=True)
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
            'A5': 148 / 210,
            'A5bld': 6.09/8.66,  # A5 with 0.13in bleed
        }
        if self.size == 'p':
            self.aspect_ratio = page_aspects[self.book.options['paper size']]
        elif self.size == 'pr':
            self.aspect_ratio = 1/page_aspects[self.book.options['paper size']]
        elif self.size == 's':
            self.aspect_ratio = page_aspects[self.book.options['paper size']]*2

    def save_insert(self):
        im = Image.open(self.path_o + self.out_file_name).convert('RGB')
        self.out_file_name = mod_file_extension(self.file_name, '.pdf')
        w_i, h_i = im.size
        aspect_ratio_i = w_i / h_i
        if aspect_ratio_i < self.aspect_ratio:
            h = w_i / self.aspect_ratio
            w = w_i
            h_adj = (h_i - h) / 2
            im = im.crop((0, 0 + h_adj, w_i, h_i - h_adj))
        else:
            h = h_i
            w = h_i * self.aspect_ratio
            w_adj = (w_i - w) / 2
            im = im.crop((0 + w_adj, 0, w_i - w_adj, h_i))

        if self.size == 's':
            im1 = im.crop((0, 0, w / 2, h))
            im2 = im.crop((w / 2, 0, w, h))
            im1.save(self.path_o + self.out_file_name, 'PDF', resolution=100.0, save_all=True, append_images=[im2])
        else:
            im.save(self.path_o + self.out_file_name, 'PDF', resolution=100.0, save_all=True)


if __name__ == '__main__':
    sys.exit()
