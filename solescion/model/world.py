from __future__ import division

from pymunk import Body, inf, init_pymunk, Space

from solescion.model.material import granite


class World(object):
    "Container for everything in the model, eg: Rooms and Chunks"

    def __init__(self):
        # pylint: disable-msg=W0212
        #   Access to a protected member '_space': ack
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, 0)
        self.space._space.contents.elasticIterations = 10
        self.static_body = Body(inf, inf)

        self.rooms = {}
        self.ents = set()
        self.chunks = set()
        self.player = None

        self.material = granite


    def add_to_pymunk(self):
        for room in self.rooms.itervalues():
            room.add_to_body(self.space, self.static_body)


    def add_chunk(self, chunk, position, angle=0):
        chunk.add_to_space(self.space, position, angle)
        self.chunks.add(chunk)


    def add_ent(self, ent, position, angle=0.0):
        ent.body.position = position
        ent.body.angle = angle
        self.space.add(ent.body)
        for shape in ent.shapes:
            self.space.add(shape)
        self.ents.add(ent)


    def gravity(self):
        for chunk in self.chunks:
            chunk.body.apply_impulse(-chunk.position/10.0, (0,0))
        for ent in self.ents:
            ent.body.apply_impulse(-ent.position/10.0, (0,0))


    def tick(self, delta_t):
        if hasattr(self, 'player'):
            self.player.move()
        self.gravity()
        self.space.step(delta_t)

