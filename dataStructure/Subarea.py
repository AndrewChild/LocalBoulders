"""
Local Boulders Guidebook builder v0.6
"""
import sys
from collections import OrderedDict
from dataStructure.base_classes.LBItem import LBItem
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Subarea(LBItem):
    __class_id: ClassVar[str] = 'subareas'
    ref: ClassVar[str] = 'sa'
    class_name: ClassVar[str] = 'sub area'

    def __post_init__(self):
        super().__post_init__()
        self.area = self.parent
        self.book = self.parent.book
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


if __name__ == '__main__':
    sys.exit()
