"""
Local Boulders Guidebook builder v0.6
Data Structures

This file holds all of the data strucutres used in the Local Boulders python scripts
"""
import os.path
import sys
from datetime import datetime
from topo import update_svg
from genLaTeX import gen_book_LaTeX
from lbResources import genHistogram, get_grade_atts, create_qr
from collections import OrderedDict
from PIL import Image


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
        elif size == 's':
            self.aspect_ratio = 1/self.page_aspects[self.book.options['paper size']]

    def save_insert(self):
        im = Image.open(self.path_o + self.out_file_name)
        self.out_file_name = self.file_name.split('.')[0] + '.pdf'
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
            self.out_file_name = file_name.split('.')[0] + '_c.png'

        self.scale = self.photo_scales[self.size]

    def update(self):
        update_svg(self)
        if self.size == 'p' or self.size == 's':
            self.save_insert()


class Book(Item):
    __class_id = 'books'
    ref = 'bk'
    class_name = 'book'
    area_colors = ['BrickRed', 'RoyalPurple', 'BurntOrange', 'Aquamarine', 'RubineRed', 'PineGreen']
    area_colors_hex = ['#CB4154', '#7851A9', '#CC5500', '#00B5BD', '#E0115F', '#01796F']
    __path_defaults = {
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
    __option_defaults = {
        'subarea_numbering': True,
        # if yes route numbering resets at zero for each sub area, if no it restarts for each area
        'paper size': 'A5',
        # controls cropping of p (page) and s (spread) action photos A5 is the only option right now
        'include_action_photos': True,
    }

    def __init__(self, name, file_name='guideBook', description='', item_id=None, repo='', dl='', collaborators=[],
                 subarea_numbering=True, paths={}, options={}, format_options=[], gps=None):
        self.paths = {**self.__path_defaults, **paths}
        self.options = {**self.__option_defaults, **options}
        super().__init__(name=name, parent=None, description=description, item_id=item_id,
                         format_options=format_options, paths=self.paths, options=self.options, gps=gps)
        self.file_name = file_name
        self.areas = OrderedDict()
        self.subareas = OrderedDict()
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()
        self.climbs = OrderedDict()  # container for routes and variations
        self.all_photos = []  # container for all action and scenery photos in book
        self.all_maps = []  # container for all layout maps and topos in book

        self.date = datetime.today().strftime('%Y-%m-%d')
        self.repo = repo
        self.dl = dl
        self.collaborators = collaborators
        self.subarea_numbering = subarea_numbering

        if dl:
            create_qr(self.paths['qr_o'], dl, f'{self.item_id}')

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
        for area in self.areas.values():
            area.update()
        for map_item in self.all_maps:
            map_item.update()


class Area(Item):
    __class_id = 'areas'
    ref = 'a'
    class_name = 'area'

    def __init__(self, name, parent, description='', item_id=None, gps=None, format_options=[], note=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id,
                         format_options=format_options, gps=gps)
        self.color = ''
        self.color_hex = ''
        self.note = note
        self.book = parent
        self.book.assign_to_dic(self.__class_id, self)
        self.subareas = OrderedDict()
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()

    def histogram(self):
        genHistogram(self)

    def update(self):
        ct = 0
        for area in self.parent.areas.values():
            if area.item_id == self.item_id:
                area_colors = self.parent.area_colors
                area_colors_hex = self.parent.area_colors_hex
                self.color = area_colors[ct % len(area_colors)]
                self.color_hex = area_colors_hex[ct % len(area_colors_hex)]
            ct = ct + 1


class Subarea(Item):
    __class_id = 'subareas'
    ref = 'sa'
    class_name = 'sub area'

    def __init__(self, name, parent, description='', item_id=None, gps=None, format_options=[], note=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id,
                         format_options=format_options, gps=gps)
        self.note = note
        self.area = parent
        self.book = parent.book
        self.book.assign_to_dic(self.__class_id, self)
        self.area.assign_to_dic(self.__class_id, self)
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()

    def getSubAreaLtr(self):
        """returns the guidebook letter id of sub area"""
        ct = 65  # start counter on the unicode number encoding for the 'A' character
        for sub_area in self.parent.subareas.values():
            if sub_area.item_id == self.item_id:
                return chr(ct)
            ct = ct + 1


class Formation(Item):
    __class_id = 'formations'
    ref = 'bd'
    class_name = 'formation'

    def __init__(self, name, parent, description='', item_id=None, format_options=[], gps=None, note=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id,
                         format_options=format_options, gps=gps)
        self.note = note
        self.subarea = parent
        self.book = parent.book
        self.area = parent.area
        self.book.assign_to_dic(self.__class_id, self)
        self.area.assign_to_dic(self.__class_id, self)
        self.subarea.assign_to_dic(self.__class_id, self)
        self.routes = OrderedDict()
        self.variations = OrderedDict()


class Route(Item, Climb):
    """class object for an individual route or boulder"""
    __class_id = 'routes'
    ref = 'rt'
    class_name = 'route'

    def __init__(self, name, parent, description='PLACEHOLDER', item_id=None, grade='?', rating=-1, serious=0,
                 grade_unconfirmed=False, name_unconfirmed=False, FA=None, format_options=[], gps=None):
        Item.__init__(self, name=name, parent=parent, description=description, item_id=item_id,
                      format_options=format_options, gps=gps)
        Climb.__init__(self, grade=grade, rating=rating, serious=serious, grade_unconfirmed=grade_unconfirmed,
                       name_unconfirmed=name_unconfirmed, FA=FA)
        self.boulder = parent
        self.book = parent.book
        self.area = parent.area
        self.subarea = parent.subarea
        self.book.assign_to_dic(self.__class_id, self)
        self.book.assign_to_dic('climbs', self)
        self.area.assign_to_dic(self.__class_id, self)
        self.subarea.assign_to_dic(self.__class_id, self)
        self.boulder.assign_to_dic(self.__class_id, self)
        self.variations = OrderedDict()

    def getRtNum(self, as_int=False):
        """returns the guidebook route number of the route"""
        ct = 1
        if self.options['subarea_numbering']:
            query_subareas = [self.subarea]
        else:
            query_subareas = self.area.subareas.values()
        for subArea in query_subareas:
            for boulder in subArea.formations.values():  # sub area also contains a dictionary of all routes but this has to be done in a multi step process in order to get the correct route numbering
                for route in boulder.routes.values():
                    if route.item_id == self.item_id:
                        if as_int:
                            return ct
                        else:
                            return str(ct)
                    ct = ct + 1


class Variation(Item, Climb):
    """class object for variations of routs"""
    __class_id = 'variations'
    ref = 'vr'
    class_name = 'variation'

    def __init__(self, name, parent, description='PLACEHOLDER', item_id=None, grade='?', rating=-1, serious=0,
                 grade_unconfirmed=False, name_unconfirmed=False, FA=None, format_options=[], gps=None):
        Item.__init__(self, name=name, parent=parent, description=description, item_id=item_id,
                      format_options=format_options, gps=gps)
        Climb.__init__(self, grade=grade, rating=rating, serious=serious, grade_unconfirmed=grade_unconfirmed,
                       name_unconfirmed=name_unconfirmed, FA=FA)
        self.route = parent
        self.book = parent.book
        self.area = parent.area
        self.subarea = parent.subarea
        self.boulder = parent.boulder
        self.book.assign_to_dic(self.__class_id, self)
        self.book.assign_to_dic('climbs', self)
        self.area.assign_to_dic(self.__class_id, self)
        self.subarea.assign_to_dic(self.__class_id, self)
        self.boulder.assign_to_dic(self.__class_id, self)
        self.route.assign_to_dic(self.__class_id, self)

    def getRtNum(self):
        """returns the guidebook route number of the variation"""
        ct = 97  # start counter on the unicode number encoding for the 'a' character
        for variation in self.parent.variations.values():
            if variation.item_id == self.item_id:
                return self.parent.getRtNum() + chr(ct)
            ct = ct + 1


class Photo(ItemImage):
    """class object for general photos (action, scenery, etc.)"""
    __class_id = 'photos'
    ref = 'pt'
    class_name = 'photo'

    def __init__(self, name, parent, file_name, description=None, item_id=None, size='h', loc='b', credit='',
                 route=None, format_options=[], paths={}):
        super().__init__(name=name, parent=parent, file_name=file_name, description=description, item_id=item_id,
                         size=size, loc=loc, format_options=format_options, paths=paths)
        self.credit = credit
        self.route = route
        self.book.all_photos.append(self)
        self.parent.photos.append(self)

        if self.size == 'p' or self.size == 's':
            self.save_insert()


class Topo(ItemMap):
    """class object for route topos"""
    __class_id = 'topos'
    ref = 'tp'
    class_name = 'topo'

    def __init__(self, name, parent, file_name, description=None, item_id=None, routes={}, layers=[], border='',
                 size='h', loc='b', out_file_name=None, format_options=[], paths={}):
        super().__init__(name=name, parent=parent, file_name=file_name, path_id='topo', description=description,
                         item_id=item_id, size=size, loc=loc, out_file_name=out_file_name,
                         format_options=format_options,
                         paths=paths, layers=layers, border=border)
        self.routes = routes.copy()  # not sure if this is necessary

        for route in routes.values():
            route.hasTopo = True


class AreaMap(ItemMap):
    """class object for sub area maps"""
    __class_id = 'areaMaps'
    ref = 'am'
    class_name = 'area map'

    def __init__(self, name, parent, file_name, description=None, item_id=None, sub_areas={}, layers=[], border='',
                 size='h', loc='b', out_file_name=None, format_options=[], paths={}):
        super().__init__(name=name, parent=parent, file_name=file_name, path_id='area', description=description,
                         item_id=item_id, size=size, loc=loc, out_file_name=out_file_name,
                         format_options=format_options,
                         paths=paths, layers=layers, border=border)
        self.sub_areas = sub_areas.copy()  # not sure if this is necessary
        self.routes = []


class SubAreaMap(ItemMap):
    """class object for sub area maps"""
    __class_id = 'subAreaMaps'
    ref = 'sm'
    class_name = 'sub area map'

    def __init__(self, name, parent, file_name, description=None, item_id=None, routes={}, layers=[], border='',
                 size='h',
                 loc='b', out_file_name=None, format_options=[], paths={}):
        super().__init__(name=name, parent=parent, file_name=file_name, path_id='subarea', description=description,
                         item_id=item_id, size=size, loc=loc, out_file_name=out_file_name,
                         format_options=format_options,
                         paths=paths, layers=layers, border=border)
        self.routes = routes.copy()  # not sure if this is necessary


if __name__ == '__main__':
    sys.exit()
# --------------------------------
