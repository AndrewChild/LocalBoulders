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

    def __init__(self, name, parent, description='', order=-1):
        assert isinstance(parent, self._parent_class)
        self.name = name
        self._parent = parent
        self.description = description
        self.order = order

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
    def __init__(self, name, author, description='', order=-1):
        super().__init__(name, None, description, order)
        self.author = author
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.ref = 'bk'


    def gen(self):
        gen_book(self)


class Area(ModuleBaseClass):
    _plural = 'areas'

    def __init__(self, name, parent, description='', order=-1, photos=[], bannerPhoto=False):
        super().__init__(name, parent, description, order)
        self.photos = photos
        self.ref = 'a'
        self.bannerPhoto = bannerPhoto
        assert self._parent_class == Book


class Subarea(ModuleBaseClass):
    _plural = 'subareas'

    def __init__(self, name, parent, description='', order=-1, photos=[], subAreaMaps={}):
        super().__init__(name, parent, description, order)
        self.photos = photos
        self.ref = 'sa'
        self.subAreaMaps = subAreaMaps.copy()
        assert self._parent_class == Area


class Boulder(ModuleBaseClass):
    _plural = 'boulders'

    def __init__(self, name, parent, description='', order=-1, photos=[], topos={}):
        super().__init__(name, parent, description, order)
        self.photos = photos
        self.ref = 'bd'
        self.topos = topos.copy()
        assert self._parent_class == Subarea


class Route(ModuleBaseClass):
    """class object for an individual route or boulder"""
    _plural = 'routes'

    def __init__(self, name, parent, description='PLACEHOLDER', order=-1, grade='?', rating=-1, serious=0):
        super().__init__(name, parent, description, order)
        self.grade = grade
        self.rating = int(rating)
        self.serious = serious
        self.serious_string = r'\warn '*self.serious
        self.ref = 'rt'

        if grade == '?':
            self.color = 'black!20'
            self.color_hex = webcolors.name_to_hex('black')
        elif grade <= 3:
            self.color = 'green!20'
            self.color_hex = webcolors.name_to_hex('green')
        elif grade <= 5:
            self.color = 'RoyalBlue!20'
            self.color_hex = webcolors.name_to_hex('RoyalBlue')
        elif grade <= 10:
            self.color = 'Goldenrod!50'
            self.color_hex = webcolors.name_to_hex('Goldenrod')
        elif grade <= 5:
            self.color = 'red!20'
            self.color_hex = webcolors.name_to_hex('red')

        if self.rating < 0:
            self.rating_string = ''
        elif rating < 1:
            self.rating_string = r'\ding{73}'
        else:
            self.rating_string = r'\ding{72} '*self.rating


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

    def __init__(self, name, parent, description='PLACEHOLDER', order=-1, grade='?', rating=-1, serious=0):
        super().__init__(name, parent, description, order)
        self.grade = grade
        self.rating = rating
        self.serious = serious
        self.serious_string = r'\warn '*self.serious
        self.ref = 'vr'
        if grade == '?':
            self.color = 'black!20'
            self.color_hex = webcolors.name_to_hex('black')
        elif grade <= 3:
            self.color = 'green!20'
            self.color_hex = webcolors.name_to_hex('green')
        elif grade <= 5:
            self.color = 'RoyalBlue!20'
            self.color_hex = webcolors.name_to_hex('RoyalBlue')
        elif grade <= 10:
            self.color = 'Goldenrod!50'
            self.color_hex = webcolors.name_to_hex('Goldenrod')
        elif grade <= 5:
            self.color = 'red!20'
            self.color_hex = webcolors.name_to_hex('red')

        if self.rating < 0:
            self.rating_string = ''
        elif rating < 1:
            self.rating_string = r'\ding{73}'
        else:
            self.rating_string = r'\ding{72} '*self.rating

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

    def __init__(self, name, fileName, description='', order=-1):
        self.name = name
        self.description = description
        self.order = order
        self.fileName = fileName


class Topo():
    """class object for route topos"""

    def __init__(self, name, boulder, fileName, description='', order=-1, routes={}, size='h', filepath='./maps/topos/'):
        self.name = name
        self.description = description
        self.order = order
        self.fileName = fileName
        self.routes = routes.copy()
        self.boulder = boulder
        self.outFileName = fileName.split('.')[0] + '_c.png'
        self.size = size
        self.filepath = filepath

        if self.size == 'f':
            self.scale = 1.0
        else:
            self.scale = 2.0
        boulder.topos.update({self.name: self})
        update_svg(self)


class SubAreaMap():
    """class object for sub area maps"""

    def __init__(self, name, subArea, fileName, description='', order=-1, routes={}, size='h', filepath='./maps/subarea/'):
        self.name = name
        self.description = description
        self.order = order
        self.fileName = fileName
        self.routes = routes.copy()
        self.subArea = subArea
        self.outFileName = fileName.split('.')[0] + '_c.png'
        self.size = size
        self.filepath = filepath

        if self.size == 'f':
            self.scale = 1.0
        else:
            self.scale = 2.0
        subArea.subAreaMaps.update({self.name: self})
        update_svg(self)

if __name__ == '__main__':
    sys.exit()
# --------------------------------
