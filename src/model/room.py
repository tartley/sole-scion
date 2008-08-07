"Module for class 'Room'"

from utils.geometry import assert_valid_poly
from pymunk import Segment


class Room(object):
    """
    A Room is a convex polygon in the game world, defining a spatial area
    within which Entities (such as the player) may move.
    """

    def __init__(self, color, verts):
        assert_valid_poly(verts)
        self.verts = verts
        self.color = color


    def add_to_body(self, space, body):
        """Add this Room to the given Space, by creating static Segments for
        each wall"""
        for idx in range(len(self.verts) - 1):
            self._add_wall_to(space, body, self.verts[idx], self.verts[idx+1])
        self._add_wall_to(space, body, self.verts[-1], self.verts[0])


    def _add_wall_to(self, space, body, vert1, vert2):
        """Add a static Segment from vert1 to vert2 to the given Space"""
        wall = Segment(body, vert1, vert2, 0.0)
        wall.friction = 0.5
        wall.elasticity = 0.5
        space.add_static(wall)

