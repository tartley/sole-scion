"Module for the World class"

from __future__ import division

from pymunk import Body, inf, init_pymunk, Space

from model.rigidbody import RigidBody
from model.room import Room
from model.shapes.block import Block
from model.shapes.disc import Disc


class World(object):
    "Container for everything in the model, ie: Rooms and Entities"

    def __init__(self):
        init_pymunk()
        self.space = Space()
        self.space.gravity = (0, -10)
        self.staticBody = Body(inf, inf)

        self.rooms = set()
        self.rigidBodies = set()

        self.backColor = (150, 100, 50)


    def populate(self):
        "Create some demo set of Rooms and Entities"
        color = (0, 50, 100)
        verts = [
            (-12, 9),
            (+12, 15),
            (+10, 5),
            (0, -1),
            (-10, 0),
        ]
        room = Room(color, verts)
        self.add_room(room)

        disc1 = Disc(2, (0, 0))
        disc2 = Disc(1, (0, +2))
        body = RigidBody(disc1, disc2)
        self.add_rigidbody(body, (-8, 8), 0)

        if 0:
            verts = [(-1, 3), (3, 2), (2, 0), (0, 0)]
            block = Block(verts)
            body = RigidBody(block)
            self.add_rigidbody(body, (8, 5.5), 0.55)

            verts = [(-1, 2), (-1, 3), (1, 4), (2, 3), (2, 2), (1, 0), (0, 0)]
            block = Block(verts)
            body = RigidBody(block)
            self.add_rigidbody(body, (-5, 1.5), -0.1)

        verts1 = [(0, 0), (0, 3), (1, 3), (1, 0)]
        block1 = Block(verts1)
        verts2 = [(0, 0), (0, 1), (3, 1), (3, 0)]
        block2 = Block(verts2)
        body = RigidBody(block1, block2)
        self.add_rigidbody(body, (+8.0, 8.5), 0.1)


    def add_room(self, room):
        "Add 'room' to this world, and insert it into Chipmunk's Space"
        room.add_to_body(self.space, self.staticBody)
        self.rooms.add(room)


    def add_rigidbody(self, rigidbody, position, angle):
        "Add 'rigidbody' to this world, and insert it into Chipmunk's Space"
        rigidbody.add_to_space(self.space, position, angle)
        self.rigidBodies.add(rigidbody)


    def tick(self, deltaT):
        "Update the world by one frame"
        self.space.step(deltaT)


