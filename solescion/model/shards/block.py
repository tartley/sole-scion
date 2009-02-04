from pymunk import moment_for_poly, Poly

from solescion.geom.poly import (
    assert_valid, offset_verts, area, centroid,
)


class Block(object):
    """
    A convex polygonal chunk, defined by vert coords relative to its body's COG.
    """
    def __init__(
        self, material, verts, offset=None, center=False):

        assert_valid(verts)
        self.verts = verts
        if center:
            self._centralize_verts()
        if offset is not None:
            self.verts = offset_verts(self.verts, offset)
        self.material = material
        self.mass = material.density * area(verts)
        self.shape = None


    def _centralize_verts(self):
        center = centroid(self.verts)
        self.offset((-center[0], -center[1]))


    def get_moment(self):
        return moment_for_poly(self.mass, self.verts, (0, 0))


    def get_offset(self):
        return centroid(self.verts)


    def offset(self, offset):
        self.verts = offset_verts(self.verts, offset)


    def add_to_body(self, space, body):
        self.shape = Poly(
            body, self.verts, (0, 0))
        self.shape.friction = self.material.friction
        self.shape.elasticity = self.material.elasticity
        space.add(self.shape)

