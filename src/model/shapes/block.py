"Module for class 'Block'"

from pymunk import moment_for_poly, Poly
from shapely.geometry import Polygon


def is_convex(verts):
    "Return True if the given verts form a convex polygon"
    if len(verts) < 3:
        return False
    poly = Polygon(verts)
    hull = poly.convex_hull
    diff = hull.difference(poly)
    return diff.is_empty


def assert_convex(verts):
    "Raise if verts do not form a convex polygon"
    if not is_convex(verts):
        raise TypeError("verts not convex: %s" % (verts,))


class Block(object):
    "A Block is a convex polygonal shape, suitable as an Entity's shape"

    def __init__(self, x, y, verts):
        assert_convex(verts)
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

