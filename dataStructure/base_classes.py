"""
Local Boulders Guidebook builder v0.6
"""
import sys
from PIL import Image
from topo import update_svg
from lbResources import get_grade_atts, create_qr, mod_file_extension


# --------------------------------
class Item:
    """
    Base class for all items in the book hierarchy (book, area, subarea, etc.)
    """

    def __init__(self, name, parent, description='', item_id=None, format_options=[], gps=None, paths={}, options={}):
        self.name = name
        self.parent = parent
        self.paths = paths
        self.description = description
        self.item_id = item_id
        self.format_options = format_options
        self.gps = gps
        self.photos = []  # container for all action and scenery photos attached to an item
        self.maps = []  # container for all layout maps and topos attached to an item
        self.images = []  # container for all images attached to item

        if not self.item_id:
            self.item_id = name
        if not self.paths:
            self.paths = parent.paths
        else:
            if parent:
                self.paths = {**parent.paths, **paths}
        if not options:
            self.options = parent.options

        if self.gps:
            self.gps = self.gps.replace(' ', '')
            create_qr(self.paths['qr_o'], 'http://maps.google.com/maps?q=' + self.gps, f'{self.item_id}')

    def assign_to_dic(self, container, connection):
        if connection.item_id in getattr(self, container):
            raise AttributeError(f'Item id "{connection.item_id}" is not unique')
        getattr(self, container).update({connection.item_id: connection})


class Climb:
    """
    Base class for all items that contain route information (e.g. boulder problem, rope route, boulder vaiation)
    """

    def __init__(self, grade='?', rating=-1, serious=0, grade_unconfirmed=False, name_unconfirmed=False, FA=None):
        self.grade = grade
        self.rating = int(rating)
        self.serious = serious
        self.grade_unconfirmed = grade_unconfirmed
        self.name_unconfirmed = name_unconfirmed
        self.color, self.color_hex, self.gradeNum, self.grade_scale, self.grade_str = get_grade_atts(grade)
        self.hasTopo = False
        self.FA = FA


class ItemImage(Item):
    """
    Base class for all image items (photos, topos, and maps. Inherits from item
    """
    page_aspects = { # holds aspect ratios of various paper sizes. currently only A5 is supported
        'A5': 148/210
    }

    def __init__(self, name, parent, file_name, description=None, item_id=None, size='h', loc='b', format_options=[],
                 paths={}):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id,
                         format_options=format_options, paths=paths)
        self.file_name = file_name
        self.out_file_name = file_name
        self.path = self.paths['photos']
        self.path_o = self.path
        self.size = size
        self.loc = loc
        self.book = parent.book
        self.parent.images.append(self)
        self.aspect_ratio = None
        if size == 'p':
            self.aspect_ratio = self.page_aspects[self.book.options['paper size']]
        elif size in ['s', 'pr']:
            self.aspect_ratio = 1/self.page_aspects[self.book.options['paper size']]

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


class ItemMap(ItemImage):
    """
    Base class for annoted map images (topos and maps)
    """
    photo_scales = {  # this is the amount that annotations should be scaled by for each photo size. This is
        # currently hard coded for the LaTeX template
        'h': 124 / 60,  # half page width
        'f': 124 / 124,  # full page width
        'p': 124 / 148,  # page width (i.e. photo page insert)
        'pr': 124 / 210,  # page width (i.e. photo page insert)
        's': 124 / (148 * 2),  # 2-page spread
    }

    def __init__(self, name, parent, file_name, path_id, description=None, item_id=None, size='h', loc='b',
                 out_file_name=None, format_options=[], paths={}, layers=[], border=''):
        super().__init__(name=name, parent=parent, file_name=file_name, description=description, item_id=item_id,
                         size=size, loc=loc, format_options=format_options, paths=paths)
        self.layers = layers
        self.border = border
        self.book.all_maps.append(self)
        self.parent.maps.append(self)

        self.path_o = self.paths[f'{path_id}_o']
        self.path_i = self.paths[f'{path_id}_i']
        if out_file_name:
            self.out_file_name = out_file_name
        else:
            if self.size in ['p', 'pr', 's']:
                self.out_file_name = mod_file_extension(file_name, '_c.pdf')
            else:
                self.out_file_name = mod_file_extension(file_name, '_c.png')

        self.scale = self.photo_scales[self.size]

    def update(self):
        update_svg(self)
        #if self.size in ['p', 'pr', 's']:
        #    self.save_insert()


if __name__ == '__main__':
    sys.exit()
