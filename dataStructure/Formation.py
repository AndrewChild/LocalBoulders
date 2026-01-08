"""
Local Boulders Guidebook builder v0.6
"""
import sys
from collections import OrderedDict
from dataStructure.base_classes import Item


class Formation(Item):
    __class_id = 'formations'
    ref = 'bd'
    class_name = 'formation'

    def __init__(self, name, parent, description='', item_id=None, format_options=[], gps=None, note=None):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id,
                         format_options=format_options, gps=gps)
        self.note = note
        self.subarea = parent
        self.book = parent.book
        self.area = parent.area
        self.book.assign_to_dic(self.__class_id, self)
        self.area.assign_to_dic(self.__class_id, self)
        self.subarea.assign_to_dic(self.__class_id, self)
        self.routes = OrderedDict()
        self.variations = OrderedDict()


if __name__ == '__main__':
    sys.exit()
