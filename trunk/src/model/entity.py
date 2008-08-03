
class Entity(object):

    next_id = 1

    def __init__(self):
        self.id = Entity.next_id
        Entity.next_id += 1


    def add_to(self, space):
        pass

