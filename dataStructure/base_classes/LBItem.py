"""
Local Boulders Guidebook builder v0.6
"""
import sys
import qrcode
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class LBItem:
    """
    Base class for all items in the book hierarchy (book, area, subarea, etc.)
    """
    name: str
    options: Dict[str, Any] = field(default_factory=dict, kw_only=True)
    paths: Dict[str, Any] = field(default_factory=dict, kw_only=True)
    format_options: List[str] = field(default_factory=list, kw_only=True)
    description: str = field(default='', kw_only=True)
    gps: str = field(default='', kw_only=True)
    parent: object = field(default=None, kw_only=True)
    item_id: str = field(default=None, kw_only=True)
    note: str = field(default=None, kw_only=True)

    def __post_init__(self):
        self.photos = []  # container for all action and scenery photos attached to an item
        self.maps = []  # container for all layout maps and topos attached to an item
        self.images = []  # container for all images attached to item

        if not self.item_id:
            self.item_id = self.name
        if not self.paths:
            self.paths = self.parent.paths
        else:
            if self.parent:
                self.paths = {**self.parent.paths, **self.paths}
        if not self.options and self.parent:
            self.options = self.parent.options

        if self.gps:
            self.gps = self.gps.replace(' ', '')
            self.create_qr(self.paths['qr_o'], 'http://maps.google.com/maps?q=' + self.gps, f'{self.item_id}')

    def assign_to_dic(self, container, connection):
        if connection.item_id in getattr(self, container):
            raise AttributeError(f'Item id "{connection.item_id}" is not unique')
        getattr(self, container).update({connection.item_id: connection})

    def create_qr(self, path, s, name):
        qr_code = qrcode.make(s)
        qr_code.save(f'{path}{name}_qr.png')

if __name__ == '__main__':
    sys.exit()
