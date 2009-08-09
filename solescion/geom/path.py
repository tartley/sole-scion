
from pyglet.gl import GL_TRIANGLES

from loop import Loop
from tessellate import tessellate


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
            x += offset[0] * loop.get_mass()
            y += offset[1] * loop.get_mass()
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
        Adds itself to the given batch, as as single primitive of indexed
        GL_TRIANGLES. Note that Batch will aggregate all such additions into
        a single large primitive.
        '''
        if self.color:
            triangles = tessellate(self.loops)
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

