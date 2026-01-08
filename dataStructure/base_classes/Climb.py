"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes.Item import Item
from lbResources import get_grade_atts
from dataclasses import dataclass


@dataclass
class Climb(Item):
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
        self.color, self.color_hex, self.gradeNum, self.grade_scale, self.grade_str = get_grade_atts(self.grade)
        self.hasTopo = False


if __name__ == '__main__':
    sys.exit()
