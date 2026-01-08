"""
Local Boulders Guidebook builder v0.6
"""
import sys
from collections import OrderedDict
from lbResources import genHistogram
from dataStructure.base_classes.Item import Item
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Area(Item):
    __class_id: ClassVar[str] = 'areas'
    ref: ClassVar[str] = 'a'
    class_name: ClassVar[str] = 'area'

    def __post_init__(self):
        super().__post_init__()
        self.color_hex = None
        self.color = None
        self.book = self.parent
        self.book.assign_to_dic(self.__class_id, self)
        self.subareas = OrderedDict()
        self.formations = OrderedDict()
        self.routes = OrderedDict()
        self.variations = OrderedDict()

    def update(self):
        genHistogram(self)
        ct = 0
        for area in self.parent.areas.values():
            if area.item_id == self.item_id:
                area_colors = self.parent.area_colors
                area_colors_hex = self.parent.area_colors_hex
                self.color = area_colors[ct % len(area_colors)]
                self.color_hex = area_colors_hex[ct % len(area_colors_hex)]
            ct = ct + 1


if __name__ == '__main__':
    sys.exit()
