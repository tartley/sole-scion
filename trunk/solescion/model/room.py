from pymunk import Segment

from solescion.model.material import Material
from solescion.geom.poly import assert_valid, centroid


def _add_wall_to(space, body, vert1, vert2):
    wall = Segment(body, vert1, vert2, 0.0)
    wall.friction = 0.5
    wall.elasticity = 0.5
    space.add_static(wall)


class Room(object):
    """
    A Room is a convex polygon in the game world, defining a spatial area
    within which Entities (such as the player) may move.
    """

    _nextRoomId = 0

    def __init__(self, verts):
        self.id = Room._nextRoomId
        Room._nextRoomId += 1
        assert_valid(verts)
        self.verts = verts
        self.material = Material.air
        self.neighbours = {}
        self.centroid = centroid(verts)


    def attach(self, wall, other, otherwall):
        self.neighbours[wall] = other
        other.neighbours[otherwall] = self


    def add_to_body(self, space, body):
        maxwall = len(self.verts) - 1
        for idx in xrange(maxwall):
            if idx not in self.neighbours:
                _add_wall_to(
                    space, body, self.verts[idx], self.verts[idx+1])
        if maxwall not in self.neighbours:
            _add_wall_to(space, body, self.verts[-1], self.verts[0])


