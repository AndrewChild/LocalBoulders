"""
Open Project Guidebook builder v0.3
Data Structures

This file holds all of the data strucutres used in the Open Project python scripts
"""
import sys

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

class Area(ModuleBaseClass):
    # def __init__(self, name, lang):
    #     super().__init__(name, None)
    #     assert lang in ['fr', 'en']
    #     self.lang = lang
    def __init__(self, name, description='', order=-1, photos=[]):
        super().__init__(name, None, description, order)
        self.photos = photos


class Subarea(ModuleBaseClass):
    _plural = 'subareas'

    def __init__(self, name, parent, description='', order=-1, photos=[]):
        super().__init__(name, parent, description, order)
        self.photos = photos
        assert self._parent_class == Area


class Boulder(ModuleBaseClass):
    _plural = 'boulders'

    def __init__(self, name, parent, description='', order=-1, photos=[]):
        super().__init__(name, parent, description, order)
        self.photos = photos
        assert self._parent_class == Subarea


class Route(ModuleBaseClass):
    """class object for an individual route or boulder"""
    _plural = 'routes'

    def __init__(self, name, parent, description='', order=-1, grade=-1, rating=-1):
        super().__init__(name, parent, description, order)
        self.grade = grade
        self.rating = rating
        assert self._parent_class == Boulder

class Variation(ModuleBaseClass):
    """class object for variations of routs"""
    _plural = 'variations'

    def __init__(self, name, parent, description='', order=-1, grade=-1):
        super().__init__(name, parent, description, order)
        self.grade = grade
        assert self._parent_class == Route

class Photo():
    """class object for general photos (action, scenery, etc.)"""

    def __init__(self, name, fileName, description='', order=-1):
        self.name = name
        self.description = description
        self.order = order
        self.fileName = fileName


if __name__ == '__main__':
    sys.exit()
# --------------------------------