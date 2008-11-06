from pymunk import moment_for_poly, Poly

from solescion.utils.geometry import (
    assert_valid_poly, offset_verts, poly_area, poly_centroid,
)


class Block(object):
    """
    A convex polygonal chunk, defined by vert coords relative to its body's COG.
    """
    def __init__(
        self, material, verts, offset=None, center=False):

        assert_valid_poly(verts)
        self.verts = verts
        if center:
            self._centralize_verts()
        if offset is not None:
            self.verts = offset_verts(self.verts, offset)
        self.material = material
        self.mass = material.density * poly_area(verts)
        self.shape = None


    def _centralize_verts(self):
        centroid = poly_centroid(self.verts)
        self.offset((-centroid[0], -centroid[1]))


    def get_moment(self):
        return moment_for_poly(self.mass, self.verts, (0, 0))


    def get_offset(self):
        return poly_centroid(self.verts)


    def offset(self, offset):
        self.verts = offset_verts(self.verts, offset)


    def add_to_body(self, space, body):
        self.shape = Poly(
            body, self.verts, (0, 0))
        self.shape.friction = self.material.friction
        self.shape.elasticity = self.material.elasticity
        space.add(self.shape)

