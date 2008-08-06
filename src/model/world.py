"Module for the World class"

from pymunk import Body, inf, init_pymunk, Space

from model.entity import Entity
from model.room import Room
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
            (+10, 1),
            (+8, 5),
            (-8, 6),
        ]
        room = Room(color, verts)
        self.add_room(room)

        ent = Entity(Disc(1, 0, 0), 4, 1, 0)
        self.add_entity(ent)
        ent = Entity(Disc(2, 0, 0), -6, 4, 0)
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

