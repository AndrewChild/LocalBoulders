"""
Local Boulders Guidebook builder v0.6
Data Structures

This file holds all of the data strucutres used in the Local Boulders python scripts
"""
from dataStructure.base_classes import ItemMap


class SubAreaMap(ItemMap):
    """class object for sub area maps"""
    __class_id = 'subAreaMaps'
    ref = 'sm'
    class_name = 'sub area map'

    def __init__(self, name, parent, file_name, description=None, item_id=None, routes={}, layers=[], border='',
                 size='h',
                 loc='b', out_file_name=None, format_options=[], paths={}):
        super().__init__(name=name, parent=parent, file_name=file_name, path_id='subarea', description=description,
                         item_id=item_id, size=size, loc=loc, out_file_name=out_file_name,
                         format_options=format_options,
                         paths=paths, layers=layers, border=border)
        self.routes = routes.copy()  # not sure if this is necessary


if __name__ == '__main__':
    sys.exit()
