"Module for the World class"

from pymunk import Body, inf, init_pymunk, Space

from model.room import Room


class World(object):
    "Container for everything in the model, ie: Rooms and Entities"

    def __init__(self):
        init_pymunk()
        self.space = Space()
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


    def add_room(self, room):
        "Add 'room' to this world, and insert it into Chipmunk's Space"
        room.add_to(self.space, self.staticBody)
        self.rooms.add(room)


    def add_entity(self, entity):
        "Add 'entity' to this world, and insert it into Chipmunk's Space"
        entity.add_to(self.space)
        self.entities.add(entity)

