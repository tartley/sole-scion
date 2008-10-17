from __future__ import division
from math import pi, sin, cos

from pyglet.window import key
from pymunk import Body, inf, init_pymunk, PivotJoint, Space

from controller.keyboard import keystate
from model.chunk import Chunk
from model.material import (
    Material, bamboo, flesh, gold, granite, ice, rubber, steel,
)
from model.room import Room
from model.shards.block import Block
from model.shards.disc import Disc


def generate_ship():
    verts = [(-1, 0), (-2, 1), (0, 5), (2, 1), (1, 0)]
    return verts


def generate_circle(radius, numSegments):
    verts = []
    for idx in range(numSegments):
        theta = 2*pi / numSegments * idx
        verts.append((radius * sin(theta), radius * cos(theta)))
    return verts



class Player(object):

    def __init__(self):
        verts = generate_ship()
        block = Block(steel, verts)
        self.chunks = [Chunk(block)]


    def add_to_space(self, space, position, angle):
        self.chunks[0].add_to_space(space, (position[0]+1, position[1]), 0)


    def move(self):
        body = self.chunks[0].body
        if keystate[key.RIGHT]:
            torque = -3000
        elif keystate[key.LEFT]:
            torque = +3000
        else:
            torque = -body.angular_velocity * 1000
        body.torque = torque

        if keystate[key.UP]:
            body.apply_impulse(body.rotation_vector.rotated(90) * 150, (0, 0))
        elif keystate[key.DOWN]:
            body.apply_impulse(body.rotation_vector.rotated(-90) * 100, (0, 0))


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
            (-120, 90),
            (+120, 140),
            (+100, 50),
            (0, -10),
            (-100, 0),
        ]
        room = Room(verts)
        self.add_room(room)

        if 1:
            disc1 = Disc(bamboo, 20, (0, 0))
            disc2 = Disc(bamboo, 10, (0, -20))
            chunk = Chunk(disc2, disc1)
            self.add_chunk(chunk, (-40, 80))

            disc = Disc(rubber, 5)
            chunk = Chunk(disc)
            self.add_chunk(chunk, (40, 120))

            verts = [(-10, 20), (30, 20), (20, 0), (0, 0)]
            block = Block(ice, verts)
            chunk = Chunk(block)
            self.add_chunk(chunk, (80, 55), 0.55)

            verts = [(-10, 20), (-10, 30), (10, 40), (20, 30), (20, 20), (10, 0), (0, 0)]
            block = Block(granite, verts)
            chunk = Chunk(block)
            self.add_chunk(chunk, (-50, 15), -0.1)

            verts1 = [(0, 0), (0, 30), (10, 30), (10, 0)]
            block1 = Block(gold, verts1)
            verts2 = [(0, 0), (0, 10), (30, 10), (30, 0)]
            block2 = Block(gold, verts2)
            chunk = Chunk(block1, block2)
            self.add_chunk(chunk, (60, 90), 0.4)

        self.player = Player()
        self.player.add_to_space(self.space, (0, 0), 0)
        self.chunks.update(self.player.chunks)



    def add_room(self, room):
        room.add_to_body(self.space, self.staticBody)
        self.rooms.add(room)


    def add_chunk(self, chunk, position, angle=0):
        chunk.add_to_space(self.space, position, angle)
        self.chunks.add(chunk)


    def tick(self, deltaT):
        self.player.move()
        self.space.step(deltaT)

