"Module for class 'Block'"

from pymunk import moment_for_poly, Poly
from shapely.geometry import Polygon

from utils.geometry import assert_valid_poly


class Block(object):
    "A Block is a convex polygonal shape, suitable as an Entity's shape"

    def __init__(self, x, y, verts):
        assert_valid_poly(verts)
        self.offset = (x, y)
        self.verts = verts
        poly = Polygon(verts)
        self.mass = poly.area
        self.moment = moment_for_poly(self.mass, verts, self.offset)
        self.shape = None


    def add_to_body(self, space, body):
        "Create a shape to represent this block, add it to 'space' and 'body'."
        self.shape = Poly(
            body, self.verts, self.offset)
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5
        space.add(self.shape)

