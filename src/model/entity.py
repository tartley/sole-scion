"Module for class 'Entity'"

from pymunk import Body

class Entity(object):
    """
    Represents an in-game object, that has a position, orientation, and a
    shape, which provides geometry and mass.
    """

    nextId = 1

    def __init__(self, shape, x, y, rot):
        self.entId = Entity.nextId
        Entity.nextId += 1
        self.shape = shape
        self.body = Body(self.shape.mass, self.shape.moment)
        self.body.position = (x, y)
        self.body.angle = rot


    x = property(lambda self: self.body.position.x)
    y = property(lambda self: self.body.position.y)
    rot = property(lambda self: self.body.angle)


    def add_to_space(self, space):
        """
        Add this Entity to the given Chipmunk Space, as a single Body
        and one or more Shapes attached to it.
        """
        self.shape.add_to_body(space, self.body)
        space.add(self.body)

