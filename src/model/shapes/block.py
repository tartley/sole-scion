"Module for class 'Block'"

from random import randint

from pymunk import moment_for_poly, Poly

from utils.geometry import assert_valid_poly, poly_area, poly_centroid


class Block(object):
    """
    A convex polygonal shape, with an offset from it's body's COG.
    Verts are normalised on construction to be centered about (0,0),
    and offset updated in the opposite direction.
    """
    def __init__(self, verts, offset=None):
        if offset is None:
            offset = (0, 0)
        assert_valid_poly(verts)
        self.verts = verts
        self.offset = offset
        self._centralize_verts()
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
        self.offset = (
            self.offset[0] + centroid[0],
            self.offset[1] + centroid[1]
        )
        newVerts = []
        for vert in self.verts:
            newVert = (
                vert[0] - centroid[0],
                vert[1] - centroid[1],
            )
            newVerts.append(newVert)
        self.verts = newVerts


    def get_moment(self):
        "Return moment of inertia of this poly at self.offset"
        return moment_for_poly(self.mass, self.verts, self.offset)


    def add_to_body(self, space, body):
        "Create a shape to represent this block, add it to 'space' and 'body'."
        self.shape = Poly(
            body, self.verts, self.offset)
        self.shape.friction = 0.5
        self.shape.elasticity = 0.5
        space.add(self.shape)

