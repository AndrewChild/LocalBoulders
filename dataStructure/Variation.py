"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes import Item, Climb
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Variation(Climb):
    """class object for variations of routs"""
    __class_id: ClassVar[str] = 'variations'
    ref: ClassVar[str] = 'vr'
    class_name: ClassVar[str] = 'variation'

    def __post_init__(self):
        super().__post_init__()
        self.route = self.parent
        self.book = self.parent.book
        self.area = self.parent.area
        self.subarea = self.parent.subarea
        self.boulder = self.parent.boulder
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


if __name__ == '__main__':
    sys.exit()
