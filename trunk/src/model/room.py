from pymunk import Segment

from model.entity import Entity


class Room(Entity):

    def __init__(self, color, verts):
        if len(color) != 3:
            raise TypeError("bad color: %s" % (color,))
        self.color = color

        if len(verts) < 3:
            raise TypeError("need 3 or more verts")
        self.verts = verts


    def add_to(self, space, body):
        for idx in range(len(self.verts) - 1):
            self._add_wall_to(space, body, self.verts[idx], self.verts[idx+1])
        self._add_wall_to(space, body, self.verts[-1], self.verts[0])


    def _add_wall_to(self, space, body, v1, v2):
        wall = Segment(body, v1, v2, 0.0)
        space.add_static(wall)

