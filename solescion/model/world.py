from __future__ import division

from pymunk import Body, inf, init_pymunk, Space

from solescion.model.material import Material


class World(object):
    "Container for everything in the model, eg: Rooms and Chunks"

    def __init__(self):
        # pylint: disable-msg=W0212
        #   Access to a protected member '_space': ack
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, -10)
        self.space._space.contents.elasticIterations = 10
        self.static_body = Body(inf, inf)

        self.rooms = {}
        self.chunks = set()
        self.player = None

        self.material = Material.granite


    def add_to_pymunk(self):
        for room in self.rooms.itervalues():
            room.add_to_body(self.space, self.static_body)


    def add_chunk(self, chunk, position, angle=0):
        chunk.add_to_space(self.space, position, angle)
        self.chunks.add(chunk)


    def tick(self, delta_t):
        if hasattr(self, 'player'):
            self.player.move()
        self.space.step(delta_t)

