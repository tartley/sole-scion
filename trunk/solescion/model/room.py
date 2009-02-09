from pymunk import Segment

from shapely.geometry import Polygon

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
        self.polygon = Polygon(verts)
        self.material = Material.air
        self.neighbours = {}


    @property
    def verts(self):
        return list(self.polygon.exterior.coords)[:-1]


    @property
    def centroid(self):
        return tuple(self.polygon.exterior.centroid.coords[0])


    def attach(self, wall, other, otherwall):
        self.neighbours[wall] = other
        other.neighbours[otherwall] = self


    def add_to_body(self, space, body):
        verts = self.polygon.exterior.coords
        maxwall = len(verts) - 1
        for idx in xrange(maxwall):
            if idx not in self.neighbours:
                _add_wall_to(space, body, verts[idx], verts[idx+1])

