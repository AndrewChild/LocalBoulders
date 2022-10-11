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

# --------------------------------
class ModuleMetaClass(type):
    """ Metaclass that is instantiated once for each class """
    _metaclass_instances = None

    def __init__(cls, name, bases, attrs):

        if cls._metaclass_instances is None:
            # First instance is ModuleBaseClass
            cls._parent_class = None
            cls._metaclass_instances = [type(None)]
        else:
            # parent class is the previously declared class
            cls._parent_class = cls._metaclass_instances[-1]

            # if not at the top of the tree, then we are our parent's child
            if cls._parent_class != type(None):
                cls._parent_class._child_class = cls

            # store this class in the list of classes
            cls._metaclass_instances.append(cls)

        # no child class yet
        cls._child_class = None

        # call our base (meta) class init
        super().__init__(name, bases, attrs)


class ModuleBaseClass(metaclass=ModuleMetaClass):
    """ Base class for each of the derived classes in our tree """

    def __init__(self, name, parent, description=''):
        assert isinstance(parent, self._parent_class)
        self.name = name
        self._parent = parent
        self.description = description

        if self._child_class is not None:
            self._children = {}

            # child class variable plural is used to add a common name
            plural = getattr(self._child_class, '_plural')
            if plural is not None:
                setattr(self, plural, self._children)

        # add self to our parents collection
        if parent is not None:
            parent._add_child(self)

        # add an access attribute for each of the nodes above us in the tree
        while parent is not None:
            setattr(self, type(parent).__name__.lower(), parent)
            parent = parent._parent

    def _add_child(self, child):
        assert isinstance(child, self._child_class)
        assert child.name not in self._children
        self._children[child.name] = child


# --------------------------------
class Book(ModuleBaseClass):
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
    def __init__(self, name, description='', repo='', dl='', collaborators=[], subarea_numbering=True, paths={}, options={}):
        super().__init__(name, None, description)
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.ref = 'bk'
        self.repo = repo
        self.dl = dl
        self.collaborators = collaborators
        self.subarea_numbering = subarea_numbering
        self.paths = {**self.__path_defaults, **paths}
        self.options = {**self.__option_defaults, **options}
        self.area_colors = ['BrickRed', 'RoyalPurple', 'BurntOrange','Aquamarine', 'Ruby', 'PineGreen']
        self.area_colors_hex = ['#CB4154', '#7851A9', '#CC5500', '#7FFFD0', '#E0115F', '#01796F']

        if dl:
            create_qr(self.paths['qr_o'] ,dl, f'{self.name}')

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
        """
        Crawls through all classes contained in book and update variables with runtime information
        """
        all_routes = []
        all_photos = []
        for area in self.areas.values():
            area.update()
            all_photos = all_photos + area.photos
            for subArea in area.subareas.values():
                all_photos = all_photos + subArea.photos
                for map in subArea.subAreaMaps:
                    update_svg(map)
                for boulder in subArea.boulders.values():
                    all_photos = all_photos + boulder.photos
                    for topo in boulder.topos:
                        update_svg(topo)
                    for route in boulder.routes.values():
                        all_routes.append(route)
                        route.num = route.getRtNum()
                        for variation in route.variations.values():
                            all_routes.append(variation)

        self.all_routes = all_routes
        self.all_photos = all_photos



class Area(ModuleBaseClass):
    _plural = 'areas'

    def __init__(self, name, parent, description='', gps=None, incomplete=False):
        super().__init__(name, parent, description)
        self.ref = 'a'
        self.color = ''
        self.color_hex = ''
        self.photos = []
        self.areaMaps = []
        self.paths = parent.paths
        self.options = parent.options
        self.incomplete = incomplete
        if gps:
            self.gps = gps.replace(' ','')
            create_qr(self.paths['qr_o'], 'http://maps.google.com/maps?q='+self.gps, f'{self.name}')

        assert self._parent_class == Book

    def histogram(self):
        genHistogram(self)

    def update(self):
        ct = 0
        for area in self._parent.areas.values():
            if area.name == self.name:
                area_colors = self._parent.area_colors
                area_colors_hex = self._parent.area_colors_hex
                self.color = area_colors[ct % len(area_colors)]
                self.color_hex = area_colors_hex[ct % len(area_colors_hex)]
            ct = ct + 1

        for map in self.areaMaps:
            update_svg(map)

class Subarea(ModuleBaseClass):
    _plural = 'subareas'

    def __init__(self, name, parent, description='', gps=None):
        super().__init__(name, parent, description)
        self.ref = 'sa'
        self.photos = []
        self.subAreaMaps = []
        self.paths = parent.paths
        self.options = parent.options
        if gps:
            self.gps = gps.replace(' ','')
            create_qr(self.paths['qr_o'], r'http://maps.google.com/maps?q='+self.gps, f'{self.name}')
        assert self._parent_class == Area

    def getSubAreaLtr(self):
        """returns the guidebook letter id of sub area"""
        ct = 65  # start counter on the unicode number encoding for the 'A' character
        for sub_area in self._parent.subareas.values():
            if sub_area.name == self.name:
                return chr(ct)
            ct = ct + 1


class Boulder(ModuleBaseClass):
    _plural = 'boulders'

    def __init__(self, name, parent, description=''):
        super().__init__(name, parent, description)
        self.ref = 'bd'
        self.topos = []
        self.photos = []
        self.paths = parent.paths
        self.options = parent.options
        assert self._parent_class == Subarea


class Route(ModuleBaseClass):
    """class object for an individual route or boulder"""
    _plural = 'routes'

    def __init__(self, name, parent, description='PLACEHOLDER', grade='?', rating=-1, serious=0,
                 grade_unconfirmed = False, name_unconfirmed = False):
        super().__init__(name, parent, description)
        self.grade = grade
        self.rating = int(rating)
        self.serious = serious
        self.grade_unconfirmed = grade_unconfirmed
        self.name_unconfirmed = name_unconfirmed
        self.paths = parent.paths
        self.options = parent.options

        self.ref = 'rt'
        self.color, self.color_hex, self.gradeNum = get_grade_atts(grade)
        self.hasTopo = False
        if self.options['topos_attached_to_routes']:
            self.topos = []

        assert self._parent_class == Boulder

    def getRtNum(self, as_int=False):
        """returns the guidebook route number of the route"""
        ct = 1
        if self.options['subarea_numbering']:
            subAreas = [self._parent._parent]
        else:
            subAreas = self._parent._parent._parent.subareas.values()
        for subArea in subAreas:
            for boulder in subArea.boulders.values():
                for route in boulder.routes.values():
                    if route.name == self.name:
                        if as_int:
                            return ct
                        else:
                            return str(ct)
                    ct = ct + 1


class Variation(ModuleBaseClass):
    """class object for variations of routs"""
    _plural = 'variations'

    def __init__(self, name, parent, description='PLACEHOLDER', grade='?', rating=-1, serious=0,
                 grade_unconfirmed=False, name_unconfirmed=False):
        super().__init__(name, parent, description)
        self.grade = grade
        self.rating = rating
        self.serious = serious
        self.grade_unconfirmed = grade_unconfirmed
        self.name_unconfirmed = name_unconfirmed
        self.paths = parent.paths
        self.options = parent.options

        self.ref = 'vr'
        self.color, self.color_hex, self.gradeNum = get_grade_atts(grade)
        self.hasTopo = False
        if self.options['topos_attached_to_routes']:
            self.topos = []

        assert self._parent_class == Route

    def getRtNum(self):
        """returns the guidebook route number of the variation"""
        ct = 97  # start counter on the unicode number encoding for the 'a' character
        for variation in self._parent.variations.values():
            if variation.name == self.name:
                return self._parent.getRtNum() + chr(ct)
            ct = ct + 1


class Photo():
    """class object for general photos (action, scenery, etc.)"""

    def __init__(self, name, parent, fileName, description='', size='h', path=None, credit=None, route=None):
        self.name = name
        self.parent = parent
        self.fileName = fileName
        self.description = description
        self.size = size
        self.credit = credit
        self.route = route
        self.paths = parent.paths
        self.options = parent.options

        if path:
            self.path = path
        else:
            self.path = parent.paths['photos']

        self.ref = 'pt'
        parent.photos.append(self)


class Topo():
    """class object for route topos"""

    def __init__(self, name, parent, fileName, description='', routes={}, layers=[], border='', size='h', path_i=None, path_o=None):
        self.name = name
        self.parent = parent
        self.fileName = fileName
        self.description = description
        self.routes = routes.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.paths = parent.paths
        self.options = parent.options

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
                if route._parent_class == Boulder:
                    route.topos.append(self)
                    break

        parent.topos.append(self)
        for route in routes.values():
            route.hasTopo = True


class AreaMap():
    """class object for sub area maps"""

    def __init__(self, name, parent, fileName, description='', sub_areas={}, layers=[], border='', size='h', path_i=None, path_o=None, outFileName=None):
        self.name = name
        self.parent = parent
        self.fileName = fileName
        self.description = description
        self.sub_areas = sub_areas.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.paths = parent.paths
        self.options = parent.options
        self.routes = []

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

        parent.areaMaps.append(self)


class SubAreaMap():
    """class object for sub area maps"""

    def __init__(self, name, parent, fileName, description='', routes={}, layers=[], border='', size='h', path_i=None, path_o=None, outFileName=None):
        self.name = name
        self.parent = parent
        self.fileName = fileName
        self.description = description
        self.routes = routes.copy()  # not sure if this is necessary
        self.layers = layers
        self.border = border
        self.size = size
        self.outFileName = outFileName
        self.paths = parent.paths
        self.options = parent.options

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

        parent.subAreaMaps.append(self)


if __name__ == '__main__':
    sys.exit()
# --------------------------------
