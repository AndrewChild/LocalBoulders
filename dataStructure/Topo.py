"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes.LBMap import LBMap
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Topo(LBMap):
    """class object for route topos"""
    __class_id: ClassVar[str] = 'topos'
    ref: ClassVar[str] = 'tp'
    class_name: ClassVar[str] = 'topo'

    def __post_init__(self):
        self.path_id = 'topo'
        super().__post_init__()
        for route in self.routes.values():
            route.hasTopo = True


if __name__ == '__main__':
    sys.exit()
