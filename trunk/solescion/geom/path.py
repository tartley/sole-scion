
from solescion.geom.loop import Loop


class GeomPath(object):
    '''
    A Path is a list of loops.
    '''
    def __init__(self, loops=None):
        if loops is None:
            loops = []
        self.loops = [Loop(loop) for loop in loops]


    def get_area(self):
        return sum(loop.get_area() for loop in self.loops)


    def get_mass(self):
        return sum(loop.get_mass() for loop in self.loops)


    def get_centroid(self):
        x, y = 0, 0
        for loop in self.loops:
            offset = loop.get_centroid()
            x += offset[0] * loop.get_area()
            y += offset[1] * loop.get_area()
        if len(self.loops) > 0:
            area = self.get_area()
            x /= area
            y /= area
        return (x, y)


    def get_moment(self):
        return sum(loop.get_moment() for loop in self.loops)


    def offset(self, x, y):
        for loop in loops:
            loop.offset(offset)


    def offset_to_origin(self):
        x, y = self.get_centroid()
        for loop in self.loops:
            loop.offset(-x, -y)


