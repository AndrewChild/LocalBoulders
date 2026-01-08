"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes import Item, Climb


class Variation(Item, Climb):
    """class object for variations of routs"""
    __class_id = 'variations'
    ref = 'vr'
    class_name = 'variation'

    def __init__(self, name, parent, description='PLACEHOLDER', item_id=None, grade='?', rating=-1, serious=0,
                 grade_unconfirmed=False, name_unconfirmed=False, FA=None, format_options=[], gps=None):
        Item.__init__(self, name=name, parent=parent, description=description, item_id=item_id,
                      format_options=format_options, gps=gps)
        Climb.__init__(self, grade=grade, rating=rating, serious=serious, grade_unconfirmed=grade_unconfirmed,
                       name_unconfirmed=name_unconfirmed, FA=FA)
        self.route = parent
        self.book = parent.book
        self.area = parent.area
        self.subarea = parent.subarea
        self.boulder = parent.boulder
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
