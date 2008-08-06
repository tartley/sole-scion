"Module for class 'Disc'"

from math import pi

from pymunk import Circle, moment_for_circle


class Disc(object):
    "Represents a circular shape. Can add itself to a given body and space."

    def __init__(self, x, y, radius):
        self.radius = radius
        self.offset = (x, y)
        self.mass = pi * self.radius * self.radius
        self.moment = moment_for_circle(self.mass, 0, self.radius, self.offset)
        self.shape = None


    def add_to_body(self, space, body):
        "Create a shape for this disc, add it to 'body' and to 'space'"
        self.shape = Circle(body, self.radius, self.offset)
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5
        space.add(self.shape)

