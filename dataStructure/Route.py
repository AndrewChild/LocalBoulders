"""
Local Boulders Guidebook builder v0.6
"""
import sys
from collections import OrderedDict
from dataStructure.base_classes import Item, Climb
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Route(Climb):
    """class object for an individual route or boulder"""
    __class_id: ClassVar[str] = 'routes'
    ref: ClassVar[str] = 'rt'
    class_name: ClassVar[str] = 'route'

    def __post_init__(self):
        super().__post_init__()
        self.boulder = self.parent
        self.book = self.parent.book
        self.area = self.parent.area
        self.subarea = self.parent.subarea
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
            # sub area also contains a dictionary of all routes but this has to be done in a multi step process in order to get the correct route numbering
            for boulder in subArea.formations.values():
                for route in boulder.routes.values():
                    if route.item_id == self.item_id:
                        if as_int:
                            return ct
                        else:
                            return str(ct)
                    ct = ct + 1


if __name__ == '__main__':
    sys.exit()
