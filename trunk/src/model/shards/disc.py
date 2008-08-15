"Module for class 'Disc'"

from math import pi

from pymunk import Circle, moment_for_circle


class Disc(object):
    """
    Represents a circular shape with an offset from it's body's COG.
    """

    def __init__(self, material, radius, offset=None):
        if offset == None:
            offset = (0, 0)
        self.material = material
        self.radius = radius
        self.center = offset
        self.mass = material.density * pi * self.radius * self.radius
        self.shape = None


    def get_offset(self):
        "Return this disc's offset from the center of its parent body"
        return self.center


    def offset(self, offset):
        "Add to this disc's offset from the center of its parent body"
        self.center = (
            self.center[0] + offset[0],
            self.center[1] + offset[1])


    def get_moment(self):
        "Return moment of inertia of this disc"
        return moment_for_circle(self.mass, 0, self.radius, self.center)


    def add_to_body(self, space, body):
        "Create a Shape for this disc on 'body', and add it to 'space'"
        self.shape = Circle(body, self.radius, self.center)
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5
        space.add(self.shape)

