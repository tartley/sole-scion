
from pyglet.graphics import Batch

from pymunk import Body, moment_for_poly, Poly
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
        self.batch = Batch()
        graphic.add_to_batch(self.batch)

        boundary = GeomPath(graphic.paths['boundary'].loops)
        boundary.offset_to_origin()
        self.body = Body(boundary.get_mass(), boundary.get_moment())
        self.shapes = [self.make_shape(loop) for loop in boundary.loops]


    def make_shape(self, loop):
        shape = Poly(self.body, loop.verts, (0, 0))
        shape.elasticity = 0.5
        shape.friction = 10.0
        return shape

