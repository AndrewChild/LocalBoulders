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


# --------------------------------
class Item:
    """
    Base class for all items in the book hierarchy (book, area, subarea, etc.)
    """

    def __init__(self, name, parent, description='', item_id=None):
        self.name = name
        self.parent = parent
        self.description = description
        self.item_id = item_id
        if not self.item_id:
            self.item_id = name

    def assign_to_dic(self, container, connection):
        if connection.item_id in getattr(self, container):
            raise AttributeError(f'Item id "{connection.item_id}" is not unique')
        getattr(self, container).update({connection.item_id: connection})


class Climb:
    """
    Base class for all items that contain route information (e.g. boulder problem, rope route, boulder vaiation)  
    """

    def __init__(self, grade='?', rating=-1, serious=0, grade_unconfirmed=False, name_unconfirmed=False):
        self.grade = grade
        self.rating = int(rating)
        self.serious = serious
        self.grade_unconfirmed = grade_unconfirmed
        self.name_unconfirmed = name_unconfirmed
        self.color, self.color_hex, self.gradeNum, self.grade_scale = get_grade_atts(grade)
        self.hasTopo = False


class Book(Item):
    __class_id = 'books'
    ref = 'bk'
    area_colors = ['BrickRed', 'RoyalPurple', 'BurntOrange', 'Aquamarine', 'RubineRed', 'PineGreen']
    area_colors_hex = ['#CB4154', '#7851A9', '#CC5500', '#7FFFD0', '#E0115F', '#01796F']
    __path_defaults = {
        'histogram_o': './maps/plots/',
        'qr_o': './maps/qr/',
        'topo_i': './maps/topos/',
        'topo_o': './maps/topos/',
        'subarea_i': './maps/subarea/',
        'subarea_o': './maps/subarea/',
        'area_i': './maps/area/',
        'area_o': './maps/area/',
        'photos': './images/'
    }
    __option_defaults = {
        'subarea_numbering': True,
        'topos_attached_to_routes': False,
    }

    def __init__(self, name, description='', item_id=None, repo='', dl='', collaborators=[], subarea_numbering=True,
                 paths={}, options={}):
        super().__init__(name=name, parent=None, description=description, item_id=item_id)
        self.areas = OrderedDict()
        self.subareas = OrderedDict()
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()
        self.climbs = OrderedDict()  # container for routes and variations
        self.photos = []  # container for all photos in book

        self.date = datetime.today().strftime('%Y-%m-%d')
        self.repo = repo
        self.dl = dl
        self.collaborators = collaborators
        self.subarea_numbering = subarea_numbering
        self.paths = {**self.__path_defaults, **paths}
        self.options = {**self.__option_defaults, **options}

        if dl:
            create_qr(self.paths['qr_o'], dl, f'{self.name}')

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
        for subArea in self.subareas.values():
            for subAreaMap in subArea.subAreaMaps:
                update_svg(subAreaMap)
        for formation in self.formations.values():
            for topo in formation.topos:
                update_svg(topo)



class Area(Item):
    __class_id = 'areas'
    ref = 'a'

    def __init__(self, name, parent, description='', item_id=None, gps=None, incomplete=False):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id)
        self.color = ''
        self.color_hex = ''
        self.paths = parent.paths
        self.options = parent.options
        self.incomplete = incomplete
        self.book = parent
        self.book.assign_to_dic(self.__class_id, self)
        self.subareas = OrderedDict()
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()
        self.photos = []
        self.areaMaps = []
        if gps:
            self.gps = gps.replace(' ', '')
            create_qr(self.paths['qr_o'], 'http://maps.google.com/maps?q=' + self.gps, f'{self.name}')

    def histogram(self):
        genHistogram(self)
        genHistogram(self)

    def update(self):
        ct = 0
        for area in self.parent.areas.values():
            if area.name == self.name:
                area_colors = self.parent.area_colors
                area_colors_hex = self.parent.area_colors_hex
                self.color = area_colors[ct % len(area_colors)]
                self.color_hex = area_colors_hex[ct % len(area_colors_hex)]
            ct = ct + 1

        for areaMap in self.areaMaps:
            update_svg(areaMap)


class Subarea(Item):
    __class_id = 'subareas'
    ref = 'sa'

    def __init__(self, name, parent, description='', item_id=None, gps=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id)
        self.paths = parent.paths
        self.options = parent.options
        self.area = parent
        self.book = parent.book
        self.book.assign_to_dic(self.__class_id, self)
        self.area.assign_to_dic(self.__class_id, self)
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()
        self.photos = []
        self.subAreaMaps = []
        if gps:
            self.gps = gps.replace(' ', '')
            create_qr(self.paths['qr_o'], r'http://maps.google.com/maps?q=' + self.gps, f'{self.name}')

    def getSubAreaLtr(self):
        """returns the guidebook letter id of sub area"""
        ct = 65  # start counter on the unicode number encoding for the 'A' character
        for sub_area in self.parent.subareas.values():
            if sub_area.name == self.name:
                return chr(ct)
            ct = ct + 1


class Formation(Item):
    __class_id = 'formations'
    ref = 'bd'

    def __init__(self, name, parent, description='', item_id=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id)
        self.subarea = parent
        self.book = parent.book
        self.area = parent.area
        self.book.assign_to_dic(self.__class_id, self)
        self.area.assign_to_dic(self.__class_id, self)
        self.subarea.assign_to_dic(self.__class_id, self)
        self.routes = OrderedDict()
        self.variations = OrderedDict()
        self.topos = []
        self.photos = []
        self.paths = parent.paths
        self.options = parent.options


class Route(Item, Climb):
    """class object for an individual route or boulder"""
    __class_id = 'routes'
    ref = 'rt'

    def __init__(self, name, parent, description='PLACEHOLDER', item_id=None, grade='?', rating=-1, serious=0,
                 grade_unconfirmed=False, name_unconfirmed=False):
        Item.__init__(self, name=name, parent=parent, description=description, item_id=item_id)
        Climb.__init__(self, grade=grade, rating=rating, serious=serious, grade_unconfirmed=grade_unconfirmed,
                       name_unconfirmed=name_unconfirmed)
        self.paths = parent.paths
        self.options = parent.options
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
        if self.options['topos_attached_to_routes']:
            self.topos = []

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
                    if route.name == self.name:
                        if as_int:
                            return ct
                        else:
                            return str(ct)
                    ct = ct + 1


class Variation(Item, Climb):
    """class object for variations of routs"""
    __class_id = 'variations'
    ref = 'vr'

    def __init__(self, name, parent, description='PLACEHOLDER', item_id=None, grade='?', rating=-1, serious=0,
                 grade_unconfirmed=False, name_unconfirmed=False):
        Item.__init__(self, name=name, parent=parent, description=description, item_id=item_id)
        Climb.__init__(self, grade=grade, rating=rating, serious=serious, grade_unconfirmed=grade_unconfirmed,
                       name_unconfirmed=name_unconfirmed)
        self.paths = parent.paths
        self.options = parent.options
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
        if self.options['topos_attached_to_routes']:
            self.topos = []

    def getRtNum(self):
        """returns the guidebook route number of the variation"""
        ct = 97  # start counter on the unicode number encoding for the 'a' character
        for variation in self.parent.variations.values():
            if variation.name == self.name:
                return self.parent.getRtNum() + chr(ct)
            ct = ct + 1


class Photo(Item):
    """class object for general photos (action, scenery, etc.)"""
    __class_id = 'photos'
    ref = 'pt'

    def __init__(self, name, parent, fileName, description='', item_id=None, size='h', path=None, credit=None,
                 route=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id)
        self.fileName = fileName
        self.size = size
        self.credit = credit
        self.route = route
        self.paths = parent.paths
        self.options = parent.options
        self.book = parent.book
        self.book.photos.append(self)
        self.parent.photos.append(self)

        if path:
            self.path = path
        else:
            self.path = parent.paths['photos']


class Topo(Item):
    """class object for route topos"""
    __class_id = 'topos'
    ref = 'tp'

    def __init__(self, name, parent, fileName, description='', item_id=None, routes={}, layers=[], border='', size='h',
                 path_i=None,
                 path_o=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id)
        self.fileName = fileName
        self.routes = routes.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.paths = parent.paths
        self.options = parent.options
        self.parent.topos.append(self)

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

        if self.options['topos_attached_to_routes']:
            for route in self.routes.values():
                route.topos.append(self)
                break

        for route in routes.values():
            route.hasTopo = True


class AreaMap(Item):
    """class object for sub area maps"""
    __class_id = 'areaMaps'
    ref = 'am'

    def __init__(self, name, parent, fileName, description='', item_id=None, sub_areas={}, layers=[], border='',
                 size='h',
                 path_i=None, path_o=None, outFileName=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id)
        self.fileName = fileName
        self.sub_areas = sub_areas.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.paths = parent.paths
        self.options = parent.options
        self.routes = []
        self.parent.areaMaps.append(self)

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

    def __init__(self, name, parent, fileName, description='', item_id=None, routes={}, layers=[], border='', size='h',
                 path_i=None,
                 path_o=None, outFileName=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id)
        self.fileName = fileName
        self.routes = routes.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.outFileName = outFileName
        self.paths = parent.paths
        self.options = parent.options
        self.parent.subAreaMaps.append(self)

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
