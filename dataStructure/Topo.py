"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes import ItemMap


class Topo(ItemMap):
    """class object for route topos"""
    __class_id = 'topos'
    ref = 'tp'
    class_name = 'topo'

    def __init__(self, name, parent, file_name, description=None, item_id=None, routes={}, layers=[], border='',
                 size='h', loc='b', out_file_name=None, format_options=[], paths={}):
        super().__init__(name=name, parent=parent, file_name=file_name, path_id='topo', description=description,
                         item_id=item_id, size=size, loc=loc, out_file_name=out_file_name,
                         format_options=format_options,
                         paths=paths, layers=layers, border=border)
        self.routes = routes.copy()  # not sure if this is necessary

        for route in routes.values():
            route.hasTopo = True


if __name__ == '__main__':
    sys.exit()
