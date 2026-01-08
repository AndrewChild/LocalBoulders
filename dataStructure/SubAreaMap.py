"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes import ItemMap
from dataclasses import dataclass
from typing import Dict, Any, ClassVar


@dataclass
class SubAreaMap(ItemMap):
    """class object for sub area maps"""
    __class_id: ClassVar[str] = 'subAreaMaps'
    ref: ClassVar[str] = 'sm'
    class_name: ClassVar[str] = 'sub area map'

    def __post_init__(self):
        self.path_id = 'subarea'
        super().__post_init__()

if __name__ == '__main__':
    sys.exit()
