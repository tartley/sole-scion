from __future__ import division

from pymunk import Body, inf, init_pymunk, Space

from model.chunk import Chunk
from model.material import gold, granite, bamboo, ice, rubber
from model.room import Room
from model.shards.block import Block
from model.shards.disc import Disc


class World(object):
    "Container for everything in the model, eg: Rooms and Chunks"

    def __init__(self):
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, -10)
        self.staticBody = Body(inf, inf)

        self.rooms = set()
        self.chunks = set()

        self.material = granite


    def populate(self):
        "Create some demo set of Rooms and Entities"
        verts = [
            (-12, 9),
            (+12, 14),
            (+10, 5),
            (0, -1),
            (-10, 0),
        ]
        room = Room(verts)
        self.add_room(room)

        disc1 = Disc(bamboo, 2, (0, 0))
        disc2 = Disc(bamboo, 1, (0, -2))
        body = Chunk(disc1, disc2)
        self.add_chunk(body, (-4, 8), 0)

        disc = Disc(rubber, 0.5)
        body = Chunk(disc)
        self.add_chunk(body, (4, 12))

        verts = [(-1, 2), (3, 2), (2, 0), (0, 0)]
        block = Block(ice, verts)
        body = Chunk(block)
        self.add_chunk(body, (8, 5.5), 0.55)

        verts = [(-1, 2), (-1, 3), (1, 4), (2, 3), (2, 2), (1, 0), (0, 0)]
        block = Block(granite, verts)
        body = Chunk(block)
        self.add_chunk(body, (-5, 1.5), -0.1)

        verts1 = [(0, 0), (0, 3), (1, 3), (1, 0)]
        block1 = Block(gold, verts1)
        verts2 = [(0, 0), (0, 1), (3, 1), (3, 0)]
        block2 = Block(gold, verts2)
        body = Chunk(block1, block2)
        self.add_chunk(body, (+6.0, 9.0), 0.4)


    def add_room(self, room):
        room.add_to_body(self.space, self.staticBody)
        self.rooms.add(room)


    def add_chunk(self, chunk, position, angle=0):
        chunk.add_to_space(self.space, position, angle)
        self.chunks.add(chunk)


    def tick(self, deltaT):
        self.space.step(deltaT)

