"Module for the World class"

from __future__ import division

from pymunk import Body, inf, init_pymunk, Space

from model.entity import Entity
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
        self.entities = set()

        self.backColor = (150, 100, 50)


    def populate(self):
        "Create some demo set of Rooms and Entities"
        color = (0, 50, 100)
        verts = [
            (-10, 0),
            (0, -1),
            (+10, 5),
            (+12, 15),
            (-12, 9),
        ]
        room = Room(color, verts)
        self.add_room(room)

        ent = Entity(Disc(0, 0, 0.25), -8, 5, 0)
        self.add_entity(ent)
        ent = Entity(Disc(0, 0, 0.5), -7, 5, 0)
        self.add_entity(ent)
        ent = Entity(Disc(0, 0, 0.75), -5, 5, 0)
        self.add_entity(ent)
        ent = Entity(Disc(0, 0, 1), -3, 5, 0)
        self.add_entity(ent)
        ent = Entity(Disc(0, 0, 2), 0, 5, 0)
        self.add_entity(ent)
        ent = Entity(Disc(0, 0, 4), 7, 9, 0)
        self.add_entity(ent)

        verts = [(-1, 3), (3, 2), (2, 0), (0, 0)]
        ent = Entity(Block(0, 0, verts), 0, 8, 0)
        self.add_entity(ent)

        verts = [(-1, 2), (-1, 3), (1, 4), (2, 3), (2, 2), (1, 0), (0, 0)]
        verts.reverse()
        ent = Entity(Block(0, 0, verts), -3, 7, 0)
        self.add_entity(ent)

        verts = [(0, 0), (0, 1), (1, 1), (1, 0)]
        ent = Entity(Block(0, 0, verts), -5, 3, 0)
        self.add_entity(ent)


    def add_room(self, room):
        "Add 'room' to this world, and insert it into Chipmunk's Space"
        room.add_to_body(self.space, self.staticBody)
        self.rooms.add(room)


    def add_entity(self, entity):
        "Add 'entity' to this world, and insert it into Chipmunk's Space"
        entity.add_to_space(self.space)
        self.entities.add(entity)


    def tick(self, deltaT):
        "Update the world by one frame"
        self.space.step(deltaT)

