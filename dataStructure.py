"""
Local Boulders Guidebook builder v0.6
Data Structures

This file holds all of the data strucutres used in the Local Boulders python scripts
"""
import sys
from datetime import datetime
import webcolors
from topo import update_svg
from genBook import gen_book


def get_grade_atts(grade):
    gradeNum = grade
    if grade == '?':
        color = 'black!20'
        color_hex = webcolors.name_to_hex('black')
        gradeNum = 42069 # set numeric value of unknown routes arbitrarily high
    elif grade <= 3:
        color = 'green!20'
        color_hex = webcolors.name_to_hex('green')
    elif grade <= 5:
        color = 'RoyalBlue!20'
        color_hex = webcolors.name_to_hex('RoyalBlue')
    elif grade <= 9:
        color = 'Goldenrod!50'
        color_hex = webcolors.name_to_hex('Goldenrod')
    else:
        color = 'red!20'
        color_hex = webcolors.name_to_hex('red')
    return color, color_hex, gradeNum


def get_rating_string(rating):
    if rating < 0:
        rating_string = ''
    elif rating < 1:
        rating_string = r'\ding{73}'
    else:
        rating_string = r'\ding{72} ' * rating
    return rating_string

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
    def __init__(self, name, author, description=''):
        super().__init__(name, None, description)
        self.author = author
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.ref = 'bk'
        # self.routesAlph = []
        # self.routesGrade = []

    def gen(self):
        allRoutes = []
        allPhotos = []
        for area in self.areas.values():
            allPhotos = allPhotos + area.photos
            for subArea in area.subareas.values():
                allPhotos = allPhotos + subArea.photos
                for boulder in subArea.boulders.values():
                    allPhotos = allPhotos + boulder.photos
                    for route in boulder.routes.values():
                        allRoutes.append(route)
                        for variation in route.variations.values():
                            allRoutes.append(variation)

        self.allRoutes = allRoutes
        self.allPhotos = allPhotos
        # routesAlph = allRoutes.sort(key=lambda x: x.name)
        # routesGrade = allRoutes.sort(key=lambda x: (x.gradeNum, x.rating))
        self.allPhotos = allPhotos


        gen_book(self)


class Area(ModuleBaseClass):
    _plural = 'areas'

    def __init__(self, name, parent, description=''):
        super().__init__(name, parent, description)
        self.ref = 'a'
        self.photos = []
        assert self._parent_class == Book


class Subarea(ModuleBaseClass):
    _plural = 'subareas'

    def __init__(self, name, parent, description=''):
        super().__init__(name, parent, description)
        self.ref = 'sa'
        self.photos = []
        self.subAreaMaps = []
        assert self._parent_class == Area


class Boulder(ModuleBaseClass):
    _plural = 'boulders'

    def __init__(self, name, parent, description=''):
        super().__init__(name, parent, description)
        self.ref = 'bd'
        self.topos = []
        self.photos = []
        assert self._parent_class == Subarea


class Route(ModuleBaseClass):
    """class object for an individual route or boulder"""
    _plural = 'routes'

    def __init__(self, name, parent, description='PLACEHOLDER', grade='?', rating=-1, serious=0):
        super().__init__(name, parent, description)
        self.grade = grade
        self.rating = int(rating)
        self.serious = serious

        self.serious_string = r'\warn ' * self.serious
        self.ref = 'rt'
        self.color, self.color_hex, self.gradeNum = get_grade_atts(grade)
        self.rating_string = get_rating_string(self.rating)

        assert self._parent_class == Boulder

    def getRtNum(self):
        """returns the guidebook route number of the route"""
        ct = 1
        for boulder in self._parent._parent.boulders.values():
            for route in boulder.routes.values():
                if route.name == self.name:
                    return str(ct)
                ct = ct + 1


class Variation(ModuleBaseClass):
    """class object for variations of routs"""
    _plural = 'variations'

    def __init__(self, name, parent, description='PLACEHOLDER', grade='?', rating=-1, serious=0):
        super().__init__(name, parent, description)
        self.grade = grade
        self.rating = rating
        self.serious = serious

        self.serious_string = r'\warn ' * self.serious
        self.ref = 'vr'
        self.color, self.color_hex, self.gradeNum = get_grade_atts(grade)
        self.rating_string = get_rating_string(self.rating)

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

    def __init__(self, name, parent, fileName, description='', size='h', filepath='./images/', credit=None, route=None):
        self.name = name
        self.parent = parent
        self.fileName = fileName
        self.description = description
        self.size = size
        self.filepath = filepath
        self.credit = credit
        self.route = route

        self.ref = 'pt'
        if route:
            self.latexRef = ' (See Page \\pageref{{{}:{}}})'.format(route.ref, route.name)
        else:
            self.latexRef = ''

        parent.photos.append(self)


class Topo():
    """class object for route topos"""

    def __init__(self, name, parent, fileName, description='', routes={}, size='h', filepath='./maps/topos/'):
        self.name = name
        self.parent = parent
        self.fileName = fileName
        self.description = description
        self.routes = routes.copy()  # not sure if this is necessary
        self.size = size
        self.filepath = filepath

        self.outFileName = fileName.split('.')[0] + '_c.png'

        if self.size == 'f':
            self.scale = 1.0
        else:
            self.scale = 2.0

        parent.topos.append(self)
        update_svg(self)


class SubAreaMap():
    """class object for sub area maps"""

    def __init__(self, name, parent, fileName, description='', routes={}, size='h', filepath='./maps/subarea/'):
        self.name = name
        self.parent = parent
        self.fileName = fileName
        self.description = description
        self.routes = routes.copy()  # not sure if this is necessary
        self.size = size
        self.filepath = filepath

        self.outFileName = fileName.split('.')[0] + '_c.png'

        if self.size == 'f':
            self.scale = 1.0
        else:
            self.scale = 2.0

        parent.subAreaMaps.append(self)
        update_svg(self)


if __name__ == '__main__':
    sys.exit()
# --------------------------------
