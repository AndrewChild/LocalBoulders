"""
Local Boulders Guidebook builder v0.6
"""
import sys
from dataStructure.base_classes import Item


class TextInsert(Item):
    """class object for text inserts (short paragraphs/flavor text)"""
    __class_id = 'insets'
    ref = 'in'
    class_name = 'text_insert'

    def __init__(self, name, parent, description=None, item_id=None, size='h', loc='b', credit='', format_options=[], paths={}):
        super().__init__(name=name, parent=parent, description=description, item_id=item_id,
                         format_options=format_options, paths=paths)
        self.credit = credit
        self.loc = loc
        self.book = parent.book
        self.size = size
        self.parent.images.append(self)


if __name__ == '__main__':
    sys.exit()
