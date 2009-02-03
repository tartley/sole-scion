from __future__ import division
from math import pi, sin, cos

from pymunk import Body, inf, init_pymunk, Space

from solescion.model.chunk import Chunk
from solescion.model.levelbuilder import LevelBuilder
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
        self.space._space.contents.elasticIterations = 10
        self.static_body = Body(inf, inf)

        self.rooms = {}
        self.chunks = set()
        self.player = None

        self.material = Material.granite


    def add_room(self, room):
        room.add_to_body(self.space, self.static_body)
        self.rooms[room.id] = room


    def add_chunk(self, chunk, position, angle=0):
        chunk.add_to_space(self.space, position, angle)
        self.chunks.add(chunk)


    def tick(self, delta_t):
        if hasattr(self, 'player'):
            self.player.move()
        self.space.step(delta_t)

