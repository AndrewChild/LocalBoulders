"""
Local Boulders Guidebook builder v0.6
"""
import sys
from collections import OrderedDict
from lbResources import genHistogram
from dataStructure.base_classes import Item


class Area(Item):
    __class_id = 'areas'
    ref = 'a'
    class_name = 'area'

    def __init__(self, name, parent, description='', item_id=None, gps=None, format_options=[], note=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id,
                         format_options=format_options, gps=gps)
        self.color = ''
        self.color_hex = ''
        self.note = note
        self.book = parent
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
