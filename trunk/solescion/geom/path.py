
from pyglet.gl import GL_TRIANGLES, GL_LINES

from loop import Loop
from tessellate import tessellate


class GeomPath(object):
    '''
    A Path is a list of loops.
    '''
    def __init__(self, loops=None):
        if loops is None:
            loops = []
        self.loops = []
        for loop in loops:
            if not isinstance(loop, Loop):
                loop = Loop(loop)
            self.loops.append(loop)


    def get_area(self):
        return sum(loop.get_area() for loop in self.loops)


    def get_mass(self):
        return sum(loop.get_mass() for loop in self.loops)


    def get_centroid(self):
        x, y = 0, 0
        for loop in self.loops:
            loopx, loopy = loop.get_centroid()
            x += loopx * loop.get_mass()
            y += loopy * loop.get_mass()
        if len(self.loops) > 0:
            area = self.get_area()
            x /= area
            y /= area
        return (x, y)


    def get_moment(self):
        return sum(loop.get_moment() for loop in self.loops)


    def offset(self, x, y):
        for loop in self.loops:
            loop.offset(x, y)


    def offset_to_origin(self):
        x, y = self.get_centroid()
        for loop in self.loops:
            loop.offset(-x, -y)


class ColoredPath(GeomPath):

    def __init__(self):
        GeomPath.__init__(self)
        self.color = (0, 0, 0)


    def _serialise_verts(self, triangles):
        for vert in triangles:
            yield vert[0]
            yield vert[1]


    def add_to_batch(self, batch):
        '''
        Tessellate loops and add them to the given pyglet Batch as an
        indexed array of verts forming GL_TRIANGLES.
        '''
        if self.color:
            triangles = tessellate(loop.verts for loop in self.loops)
            num_verts = len(triangles)
            serial_verts = list(self._serialise_verts(triangles))
            colors = self.color * num_verts
            indices = range(num_verts)
            batch.add_indexed(
                num_verts,
                GL_TRIANGLES,
                None,
                indices,
                ('v2f/static', serial_verts),
                ('c3B/static', colors),
            )

