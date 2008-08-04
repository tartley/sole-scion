"Module of the Entity class"
from pymunk import Body, Circle

class Entity(object):
    """
    An Entity represents a single rigid body within the gameworld. It manages
    a list of circles and convex polys to be considered by Chipmunk in the
    physics of this object, and are rendered to the window to draw this entity.
    """

    nextId = 1

    def __init__(self):
        self.entId = Entity.nextId
        Entity.nextId += 1


    def add_to(self, space):
        """
        Add this Entity to the given Chipmunk Space, as a single Body
        and one or more Shapes attached to it"""
        body = Body(1, 1)
        shape = Circle(body, 1, (0, 0))
        space.add(body, shape)



