class Item():
    def __init__ (self, name, parent, description='', id=None):
        self.name = name
        self.parent = parent
        self.description = description
        self.id = id
        if not self.id:
            self.id = name
        self.test2 = {}

    def assign_to_dic(self, container, connection):
        if connection.id in getattr(self, container):
            raise AttributeError(f'Item id "{connection.id}" is not unique')
        getattr(self, container).update({connection.id: connection})

class Test(Item):
    class_id = 'test'
    def __init__(self, name, parent=None, description='', id=None):
        super().__init__(name, parent, description, id)

class Test2(Item):
    class_id = 'test2'
    def __init__(self, name, parent, description='', id=None):
        super().__init__(name, parent, description, id)
        self.cont = {}
        self.parent.assign_to_dic(self.class_id, self)


test1 = Test('test1')
testes = Test2('test2', test1)
Test2('test3', test1)
test4 = Test('test4')
Test2('test5', test4)
pass