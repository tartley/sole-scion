from pymunk import Body, inf, init_pymunk, Segment, Space

from model.room import Room


class World(object):

    def __init__(self):
        init_pymunk()
        self.space = Space()
        self.staticBody = Body(inf, inf)

        self.rooms = set()
        self.entities = set()

        self.backColor = (150, 100, 50)


    def populate(self):
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
        room.add_to(self.space, self.staticBody)
        self.rooms.add(room)


    def add_entity(self, entity):
        entity.add_to(self.space)
        self.entities.add(entity)

