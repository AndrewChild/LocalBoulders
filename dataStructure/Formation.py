"""
Local Boulders Guidebook builder v0.6
"""
import sys
from collections import OrderedDict
from dataStructure.base_classes import Item
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Formation(Item):
    __class_id: ClassVar[str] = 'formations'
    ref: ClassVar[str] = 'bd'
    class_name: ClassVar[str] = 'formation'

    def __post_init__(self):
        super().__post_init__()
        self.subarea = self.parent
        self.book = self.parent.book
        self.area = self.parent.area
        self.book.assign_to_dic(self.__class_id, self)
        self.area.assign_to_dic(self.__class_id, self)
        self.subarea.assign_to_dic(self.__class_id, self)
        self.routes = OrderedDict()
        self.variations = OrderedDict()


if __name__ == '__main__':
    sys.exit()
