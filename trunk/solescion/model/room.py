from pymunk import Segment

from solescion.model.material import air
from solescion.utils.geometry import assert_valid_poly


class Room(object):
    """
    A Room is a convex polygon in the game world, defining a spatial area
    within which Entities (such as the player) may move.
    """

    def __init__(self, verts):
        assert_valid_poly(verts)
        self.verts = verts
        self.material = air


    def add_to_body(self, space, body):
        for idx in range(len(self.verts) - 1):
            self._add_wall_to(space, body, self.verts[idx], self.verts[idx+1])
        self._add_wall_to(space, body, self.verts[-1], self.verts[0])


    def _add_wall_to(self, space, body, vert1, vert2):
        wall = Segment(body, vert1, vert2, 0.0)
        wall.friction = 0.5
        wall.elasticity = 0.5
        space.add_static(wall)

