"Module for class 'Disc'"

from math import pi

from pymunk import Circle, moment_for_circle


class Disc(object):
    """
    Represents a circular shape. Can add itself to a given body, and
    render itself using openGL primitives.
    """

    def __init__(self, radius, x, y):
        self.radius = radius
        self.x = x
        self.y = y
        self.mass = pi * self.radius * self.radius
        self.moment = moment_for_circle(self.mass, 0, self.radius, (x, y))


    def add_to_body(self, space, body):
        "Add a Circle shape representing this shape to the given space and body"
        shape = Circle(body, self.radius, (self.x, self.y))
        space.add(shape)

