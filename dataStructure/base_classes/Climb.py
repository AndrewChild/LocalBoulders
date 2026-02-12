"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes.LBItem import LBItem
from dataclasses import dataclass


@dataclass
class Climb(LBItem):
    """
    Base class for all items that contain route information (e.g. boulder problem, rope route, boulder variation)
    """
    grade: str = '?'
    description: str = "PLACEHOLDER"
    rating: int = -1
    serious: int = 0
    grade_unconfirmed: bool = False
    name_unconfirmed: bool = False
    FA: str = None

    def __post_init__(self):
        super().__post_init__()
        self.hasTopo = False


if __name__ == '__main__':
    sys.exit()
