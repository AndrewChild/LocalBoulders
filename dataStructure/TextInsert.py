"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes.LBItem import LBItem
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class TextInsert(LBItem):
    """class object for text inserts (short paragraphs/flavor text)"""
    size: str = 'h'
    loc: str = 'b'
    credit: str = None

    __class_id: ClassVar[str] = 'inserts'
    ref: ClassVar[str] = 'in'
    class_name: ClassVar[str] = 'text_insert'

    def __post_init__(self):
        super().__post_init__()
        self.book = self.parent.book
        self.parent.images.append(self)


if __name__ == '__main__':
    sys.exit()
