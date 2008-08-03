from pymunk import Body, Circle

class Entity(object):

    next_id = 1

    def __init__(self):
        self.id = Entity.next_id
        Entity.next_id += 1


    def add_to(self, space):
        body = Body(1, 1)
        shape = Circle(body, 1, (0, 0))
        space.add(body, shape)


