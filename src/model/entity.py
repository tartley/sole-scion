
class Entity(object):

    next_id = 4

    def __init__(self):
        self.id = Entity.next_id
        Entity.next_id += 1
