"""
Local Boulders Guidebook builder v0.6
Data Structures

This file holds all of the data strucutres used in the Local Boulders python scripts
"""
import sys
from dataStructure.base_classes import ItemMap


class AreaMap(ItemMap):
    """class object for sub area maps"""
    __class_id = 'areaMaps'
    ref = 'am'
    class_name = 'area map'

    def __init__(self, name, parent, file_name, description=None, item_id=None, sub_areas={}, layers=[], border='',
                 size='h', loc='b', out_file_name=None, format_options=[], paths={}):
        super().__init__(name=name, parent=parent, file_name=file_name, path_id='area', description=description,
                         item_id=item_id, size=size, loc=loc, out_file_name=out_file_name,
                         format_options=format_options,
                         paths=paths, layers=layers, border=border)
        self.sub_areas = sub_areas.copy()  # not sure if this is necessary
        self.routes = []


if __name__ == '__main__':
    sys.exit()
