
from pyglet.graphics import Batch

from pymunk import Body, moment_for_poly
from pymunk.vec2d import Vec2d

from solescion.geom.path import Path

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

        # TODO: can we not do this on load_graphics()?
        boundary = graphic.get_boundary()
        self.body = Body(boundary.get_mass(), boundary.get_moment())
        self.shapes = [loop.get_shape(self.body) for loop in boundary.loops]

