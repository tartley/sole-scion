
from pyglet.graphics import Batch

from pymunk import Body, moment_for_poly
from pymunk.vec2d import Vec2d

from solescion.geom.path import GeomPath

class GameEnt(object):

    def __init__(self, graphic):
        self.batch = None
        self.body = None
        self.shapes = []
        self.set_graphic(graphic)

    position = property(lambda self: self.body.position)

    angle = property(lambda self: self.body.angle)


    def set_graphic(self, graphic):
        print
        print 'set_graphic', graphic
        self.batch = Batch()
        graphic.add_to_batch(self.batch)

        boundary = GeomPath(graphic.paths['boundary'].loops)
        print 'boundary', len(boundary.loops)
        self.body = Body(boundary.get_mass(), boundary.get_moment())
        print 'body.mass', self.body.mass
        print 'body.moment', self.body.moment
        self.shapes = [loop.get_shape(self.body) for loop in boundary.loops]

