"""
Local Boulders Guidebook builder v0.6
"""
import sys
from collections import OrderedDict
from dataStructure.base_classes import Item, Climb


class Route(Item, Climb):
    """class object for an individual route or boulder"""
    __class_id = 'routes'
    ref = 'rt'
    class_name = 'route'

    def __init__(self, name, parent, description='PLACEHOLDER', item_id=None, grade='?', rating=-1, serious=0,
                 grade_unconfirmed=False, name_unconfirmed=False, FA=None, format_options=[], gps=None):
        Item.__init__(self, name=name, parent=parent, description=description, item_id=item_id,
                      format_options=format_options, gps=gps)
        Climb.__init__(self, grade=grade, rating=rating, serious=serious, grade_unconfirmed=grade_unconfirmed,
                       name_unconfirmed=name_unconfirmed, FA=FA)
        self.boulder = parent
        self.book = parent.book
        self.area = parent.area
        self.subarea = parent.subarea
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
            for boulder in subArea.formations.values():  # sub area also contains a dictionary of all routes but this has to be done in a multi step process in order to get the correct route numbering
                for route in boulder.routes.values():
                    if route.item_id == self.item_id:
                        if as_int:
                            return ct
                        else:
                            return str(ct)
                    ct = ct + 1


if __name__ == '__main__':
    sys.exit()
