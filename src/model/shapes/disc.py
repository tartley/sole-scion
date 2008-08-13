"Module for class 'Disc'"

from math import pi
from random import randint

from pymunk import Circle, moment_for_circle


class Disc(object):
    """
    Represents a circular shape with an offset from it's body's COG.
    """

    def __init__(self, radius, offset=None):
        if offset == None:
            offset = (0, 0)
        self.radius = radius
        self.offset = offset
        self.mass = pi * self.radius * self.radius
        self.shape = None
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))


    def get_moment(self):
        "Return moment of inertia of this disc at self.offset"
        return moment_for_circle(self.mass, 0, self.radius, self.offset)


    def add_to_body(self, space, body):
        "Create a Shape for this disc on 'body', and add it to 'space'"
        self.shape = Circle(body, self.radius, self.offset)
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5
        space.add(self.shape)

