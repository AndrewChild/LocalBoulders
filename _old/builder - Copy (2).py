"""
Open Project Guidebook builder v0.2
"""
from dataclasses import dataclass


@dataclass(eq=False, order=False)
class Climb():
    """class object for an individual route or boulder"""
    name: str
    grade: int
    Area: str
    SubArea: str
    Boulder: str
    description: str = ''
    rating: int = -1
    order: int = -1

    def __eq__(self, other):
        return self.order == other.order

    def __lt__(self, other):
        return self.order < other.order

    def __le__(self, other):
        return self.order <= other.order

    def __gt__(self, other):
        return self.order > other.order

    def __ge__(self, other):
        return self.order >= other.order



print('huh')
test1 = Climb(1, 'Octurnal', 7, 5, 'Garden', 'Methlab', 'cool')
test2 = Climb(2, 'Fight Club', 8, 5, 'Garden', 'Methlab', 'cool')
print('done')