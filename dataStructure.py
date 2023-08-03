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
        self.photos = []    # container for all action and scenery photos attached to an item
        self.maps = []      # container for all layout maps and topos attached to an item
        self.images = []    # container for all images attached to item

        if not self.item_id:
            self.item_id = name
        if not paths:
            self.paths = parent.paths
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
        'subarea_numbering': True,  # if yes route numbering resets at zero for each sub area, if no it restarts for each area
        'aspect_ratio': 'A5',       # controls cropping of p (page) and s (spread) action photos A5 is the only option right now
        'include_action_photos': True,
    }

    def __init__(self, name, filename='guideBook', description='', item_id=None, repo='', dl='', collaborators=[],
                 subarea_numbering=True, paths={}, options={}, format_options=[], gps=None):
        self.paths = {**self.__path_defaults, **paths}
        self.options = {**self.__option_defaults, **options}
        super().__init__(name=name, parent=None, description=description, item_id=item_id,
                         format_options=format_options, paths=self.paths, options=self.options, gps=gps)
        self.filename = filename
        self.areas = OrderedDict()
        self.subareas = OrderedDict()
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()
        self.climbs = OrderedDict()  # container for routes and variations
        self.all_photos = []    # container for all action and scenery photos in book
        self.all_maps = []      # container for all layout maps and topos in book

        self.date = datetime.today().strftime('%Y-%m-%d')
        self.repo = repo
        self.dl = dl
        self.collaborators = collaborators
        self.subarea_numbering = subarea_numbering

        if dl:
            create_qr(self.paths['qr_o'], dl, f'{self.item_id}')

    def gen(self):
        self._init_paths()
        self._update()
        gen_book_LaTeX(self)

    def _init_paths(self):
        """
        ensures that all paths in os.paths exist
        """
        for path in self.paths.values():
            if not os.path.exists(path):
                print(f'Creating new directory: {path}')
                os.makedirs(path)

    def _update(self):
        for area in self.areas.values():
            area.update()
        for map_item in self.all_maps:
            update_svg(map_item)


class Area(Item):
    __class_id = 'areas'
    ref = 'a'
    class_name = 'area'

    def __init__(self, name, parent, description='', item_id=None, gps=None, incomplete=False, format_options=[]):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id, format_options=format_options, gps=gps)
        self.color = ''
        self.color_hex = ''
        self.incomplete = incomplete
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

    def __init__(self, name, parent, description='', item_id=None, gps=None, format_options=[]):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id, format_options=format_options, gps=gps)
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

    def __init__(self, name, parent, description='', item_id=None, format_options=[], gps=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id, format_options=format_options, gps=gps)
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
        Item.__init__(self, name=name, parent=parent, description=description, item_id=item_id, format_options=format_options, gps=gps)
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
        Item.__init__(self, name=name, parent=parent, description=description, item_id=item_id, format_options=format_options, gps=gps)
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


class Photo(Item):
    """class object for general photos (action, scenery, etc.)"""
    __class_id = 'photos'
    ref = 'pt'
    class_name = 'photo'

    def __init__(self, name, parent, fileName, description=None, item_id=None, size='h', loc='b', path=None, credit='',
                 route=None, format_options=[]):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id, format_options=format_options)
        self.fileName = fileName
        self.size = size
        self.loc = loc
        self.credit = credit
        self.route = route
        self.book = parent.book
        self.book.all_photos.append(self)
        self.parent.photos.append(self)
        self.parent.images.append(self)

        if path:
            self.path = path
        else:
            self.path = parent.paths['photos']
        self.path_o = self.path
        self.outFileName = self.fileName
        if self.size == 'p' or self.size == 's':
            im = Image.open(self.path_o + self.fileName)
            self.fileName = self.fileName + '.pdf'
            if self.book.options['aspect_ratio'] == 'A5':
                aspect_ratio_s = 1.4139
                aspect_ratio_p = 1/aspect_ratio_s
            if size == 's':
                aspect_ratio = aspect_ratio_s
            else:
                aspect_ratio = aspect_ratio_p
            w_i, h_i = im.size
            aspect_ratio_i = w_i/h_i
            if aspect_ratio_i < aspect_ratio:
                h = w_i/aspect_ratio
                h_adj = (h_i - h)/2
                im = im.crop((0, 0+h_adj, w_i, h_i-h_adj))
            else:
                w = h_i*aspect_ratio
                w_adj = (w_i - w)/2
                im = im.crop((0+w_adj, 0, w_i-w_adj, h_i))

            if size == 's':
                w, h = im.size
                im1 = im.crop((0, 0, w/2, h))
                im2 = im.crop((w/2, 0, w, h))
                im1.save(self.path_o + self.fileName, 'PDF', resolution=100.0, save_all=True, append_images=[im2])
            else:
                im.save(self.path_o + self.fileName, 'PDF', resolution=100.0, save_all=True)


class Topo(Item):
    """class object for route topos"""
    __class_id = 'topos'
    ref = 'tp'
    class_name = 'topo'

    def __init__(self, name, parent, fileName, description=None, item_id=None, routes={}, layers=[], border='', size='h',
                 loc='b', path_i=None, path_o=None, format_options=[]):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id, format_options=format_options)
        self.fileName = fileName
        self.routes = routes.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.loc = loc
        self.book = parent.book
        self.book.all_maps.append(self)
        self.parent.maps.append(self)
        self.parent.images.append(self)

        if path_i:
            self.path_i = path_i
        else:
            self.path_i = parent.paths['topo_i']
        if path_o:
            self.path_o = path_o
        else:
            self.path_o = parent.paths['topo_o']

        self.outFileName = fileName.split('.')[0] + '_c.png'

        if self.size == 'f':
            self.scale = 1.0
        else:
            self.scale = 2.0

        for route in routes.values():
            route.hasTopo = True


class AreaMap(Item):
    """class object for sub area maps"""
    __class_id = 'areaMaps'
    ref = 'am'
    class_name = 'area map'

    def __init__(self, name, parent, fileName, description=None, item_id=None, sub_areas={}, layers=[], border='',
                 size='h', loc='b', path_i=None, path_o=None, outFileName=None, format_options=[]):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id, format_options=format_options)
        self.fileName = fileName
        self.sub_areas = sub_areas.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.loc = loc
        self.routes = []
        self.book = parent.book
        self.book.all_maps.append(self)
        self.parent.maps.append(self)
        self.parent.images.append(self)

        if path_i:
            self.path_i = path_i
        else:
            self.path_i = parent.paths['area_i']
        if path_o:
            self.path_o = path_o
        else:
            self.path_o = parent.paths['area_o']

        if not outFileName:
            self.outFileName = fileName.split('.')[0] + '_c.png'

        if self.size == 'f':
            self.scale = 1.0
        else:
            self.scale = 2.0


class SubAreaMap(Item):
    """class object for sub area maps"""
    __class_id = 'subAreaMaps'
    ref = 'sm'
    class_name = 'sub area map'

    def __init__(self, name, parent, fileName, description=None, item_id=None, routes={}, layers=[], border='', size='h',
                 loc='b', path_i=None, path_o=None, outFileName=None, format_options=[]):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id, format_options=format_options)
        self.fileName = fileName
        self.routes = routes.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.loc = loc
        self.outFileName = outFileName
        self.book = parent.book
        self.book.all_maps.append(self)
        self.parent.maps.append(self)
        self.parent.images.append(self)

        if path_i:
            self.path_i = path_i
        else:
            self.path_i = parent.paths['subarea_i']
        if path_o:
            self.path_o = path_o
        else:
            self.path_o = parent.paths['subarea_o']

        if not outFileName:
            self.outFileName = fileName.split('.')[0] + '_c.png'

        if self.size == 'f':
            self.scale = 1.0
        else:
            self.scale = 2.0


if __name__ == '__main__':
    sys.exit()
# --------------------------------
