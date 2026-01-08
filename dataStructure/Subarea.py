"""
Local Boulders Guidebook builder v0.6
"""
import sys
from collections import OrderedDict
from dataStructure.base_classes import Item


class Subarea(Item):
    __class_id = 'subareas'
    ref = 'sa'
    class_name = 'sub area'

    def __init__(self, name, parent, description='', item_id=None, gps=None, format_options=[], note=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id,
                         format_options=format_options, gps=gps)
        self.note = note
        self.area = parent
        self.book = parent.book
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
