
from pymunk import Body, Circle
from pymunk.vec2d import Vec2d


class GameEnt(object):

    def __init__(self, graphic):
        self.batch = None
        self.body = None
        self.shapes = []
        self.set_graphic(graphic)


    def _set_position(self, position):
        self.body.position = position
    position = property(lambda self: self.body.position, _set_position)
    angle = property(lambda self: self.body.angle)


    def set_graphic(self, graphic):
        self.batch = graphic.create_batch()

        self.body = Body(100, 1000)
        shape = Circle(self.body, 250, (0, 0))
        shape.elasticity = 0.5
        shape.friction = 100.0
        self.shapes = [shape]


