"Module for class 'Entity'"

from pymunk import Body

class Entity(object):
    """
    Represents an in-game object, that has a position, orientation, and a
    geometry and mass provided by its shape
    """

    nextId = 1

    def __init__(self, shape, x, y, rot):
        self.entId = Entity.nextId
        Entity.nextId += 1

        self.x = x
        self.y = y
        self.rot = rot
        self.shape = shape


    def add_to_space(self, space):
        """
        Add this Entity to the given Chipmunk Space, as a single Body
        and one or more Shapes attached to it.
        """
        body = Body(self.shape.mass, self.shape.moment)
        self.shape.add_to_body(space, body)
        space.add(body)


