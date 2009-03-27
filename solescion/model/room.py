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
        self.verts = None
        self.polygon = Polygon(verts)
        self.material = Material.air
        self.neighbours = {}


    def _set_polygon(self, poly):
        self._polygon = poly
        self.verts = list(self.polygon.exterior.coords)[:-1]

    polygon = property(lambda self: self._polygon, _set_polygon)


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

