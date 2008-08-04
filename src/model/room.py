"Module for class 'Room'"

from pymunk import Segment


class Room(object):
    """
    A Room is a convex polygon in the world, defining a spatial area within
    which Entities may exist. The Room is modelled as a list of vertices.
    When a room is inserted into a Chipmunk Space, it inserts each of its
    walls as static Segments.
    """

    def __init__(self, color, verts):
        if len(color) != 3:
            raise TypeError("bad color: %s" % (color,))
        self.color = color

        if len(verts) < 3:
            raise TypeError("need 3 or more verts")
        self.verts = verts


    def add_to(self, space, body):
        """Add this Room to the given Space, by creating static Segments for
        each wall"""

        for idx in range(len(self.verts) - 1):
            self._add_wall_to(space, body, self.verts[idx], self.verts[idx+1])
        self._add_wall_to(space, body, self.verts[-1], self.verts[0])


    def _add_wall_to(self, space, body, vert1, vert2):
        """Add a static Segment from vert1 to vert2 to the given Space"""
        wall = Segment(body, vert1, vert2, 0.0)
        space.add_static(wall)

