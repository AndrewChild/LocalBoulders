"""
Local Boulders Guidebook builder v0.6
Data Structures

This file holds all of the data strucutres used in the Local Boulders python scripts
"""
import sys
from dataStructure.base_classes import ItemMap
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class AreaMap(ItemMap):
    """class object for sub area maps"""
    __class_id: ClassVar[str] = 'areaMaps'
    ref: ClassVar[str] = 'am'
    class_name: ClassVar[str] = 'area map'

    def __post_init__(self):
        self.path_id = 'area'
        super().__post_init__()

if __name__ == '__main__':
    sys.exit()
