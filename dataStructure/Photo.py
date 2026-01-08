"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes.LBImage import LBImage
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Photo(LBImage):
    """class object for general photos (action, scenery, etc.)"""
    route: object = None
    credit: str = ''

    __class_id: ClassVar[str] = 'photos'
    ref: ClassVar[str] = 'pt'
    class_name: ClassVar[str] = 'photo'

    def __post_init__(self):
        super().__post_init__()
        self.book.all_photos.append(self)
        self.parent.photos.append(self)

        if self.size in ['p', 'pr', 's']:
            self.save_insert()


if __name__ == '__main__':
    sys.exit()
