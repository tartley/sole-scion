"Module for class 'Block'"

from random import randint

from pymunk import moment_for_poly, Poly

from utils.geometry import (
    assert_valid_poly, offset_verts, poly_area, poly_centroid,
)


class Block(object):
    """
    A convex polygonal shape, vert coords relative to it's body's COG.
    """
    def __init__(self, verts, offset=None, center=False):
        assert_valid_poly(verts)
        self.verts = verts
        if center:
            self._centralize_verts()
        if offset is not None:
            self.verts = offset_verts(self.verts, offset)
        self.mass = poly_area(verts)
        self.shape = None
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))


    def _centralize_verts(self):
        """
        Offset verts such that their centroid is (0, 0). Move self.offset
        in the opposite direction to compensate, so that this shape is
        unmoved in relation to its parent body.
        """
        centroid = poly_centroid(self.verts)
        offset = (-centroid[0], -centroid[1])
        self.verts = offset_verts(self.verts, offset)


    def get_moment(self):
        "Return moment of inertia of this poly at self.offset"
        return moment_for_poly(self.mass, self.verts, (0, 0))


    def get_offset(self):
        "Return centroid of our poly verts"
        return poly_centroid(self.verts)


    def offset(self, offset):
        self.verts = offset_verts(self.verts, offset)


    def add_to_body(self, space, body):
        "Create a shape to represent this block, add it to 'space' and 'body'."
        self.shape = Poly(
            body, self.verts, (0, 0))
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5
        space.add(self.shape)

