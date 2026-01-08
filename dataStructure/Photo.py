"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes import ItemImage


class Photo(ItemImage):
    """class object for general photos (action, scenery, etc.)"""
    __class_id = 'photos'
    ref = 'pt'
    class_name = 'photo'

    def __init__(self, name, parent, file_name, description=None, item_id=None, size='h', loc='b', credit='',
                 route=None, format_options=[], paths={}):
        super().__init__(name=name, parent=parent, file_name=file_name, description=description, item_id=item_id,
                         size=size, loc=loc, format_options=format_options, paths=paths)
        self.credit = credit
        self.route = route
        self.book.all_photos.append(self)
        self.parent.photos.append(self)

        if self.size in ['p', 'pr', 's']:
            self.save_insert()


if __name__ == '__main__':
    sys.exit()
