from __future__ import division
from math import pi, sin, cos

from pymunk import Body, inf, init_pymunk, Space

from solescion.model.chunk import Chunk
from solescion.model.material import Material
from solescion.model.player import Player
from solescion.model.room import Room
from solescion.model.shards.block import Block
from solescion.model.shards.disc import Disc


def generate_circle(radius, num_segments):
    verts = []
    for idx in range(num_segments):
        theta = 2*pi / num_segments * idx
        verts.append((radius * sin(theta), radius * cos(theta)))
    return verts



class World(object):
    "Container for everything in the model, eg: Rooms and Chunks"

    def __init__(self):
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, -10)
        self.static_body = Body(inf, inf)

        self.rooms = set()
        self.chunks = set()
        self.player = None

        self.material = Material.granite


    def populate(self):
        "Create some demo set of Rooms and Entities"
        verts = [
            (-120, 90),
            (+120, 140),
            (+100, 50),
            (0, -10),
            (-100, 0),
        ]
        room = Room(verts)
        self.add_room(room)

        disc1 = Disc(Material.bamboo, 20, (0, 0))
        disc2 = Disc(Material.bamboo, 10, (0, -20))
        chunk = Chunk(disc2, disc1)
        self.add_chunk(chunk, (-40, 80))

        disc = Disc(Material.rubber, 5)
        chunk = Chunk(disc)
        self.add_chunk(chunk, (40, 120))

        verts = [(-10, 20), (30, 20), (20, 0), (0, 0)]
        block = Block(Material.ice, verts)
        chunk = Chunk(block)
        self.add_chunk(chunk, (80, 55), 0.55)

        verts = [
            (-10, 20), (-10, 30), (10, 40), (20, 30),
            (20, 20), (10, 0), (0, 0)]
        block = Block(Material.granite, verts)
        chunk = Chunk(block)
        self.add_chunk(chunk, (-50, 15), -0.1)

        verts1 = [(0, 0), (0, 30), (10, 30), (10, 0)]
        block1 = Block(Material.gold, verts1)
        verts2 = [(0, 0), (0, 10), (30, 10), (30, 0)]
        block2 = Block(Material.gold, verts2)
        chunk = Chunk(block1, block2)
        self.add_chunk(chunk, (60, 90), 0.4)

        self.player = Player()
        self.player.add_to_space(self.space, (0, 0), 0)
        self.chunks.update(self.player.chunks)


    def add_room(self, room):
        room.add_to_body(self.space, self.static_body)
        self.rooms.add(room)


    def add_chunk(self, chunk, position, angle=0):
        chunk.add_to_space(self.space, position, angle)
        self.chunks.add(chunk)


    def tick(self, delta_t):
        if hasattr(self, 'player'):
            self.player.move()
        self.space.step(delta_t)

