from model.room import Room

class World(object):

    def __init__(self):
        self.rooms = set()


    def populate(self):
        verts = [
            (-10, 0),
            (0, -1),
            (+10, 1),
            (+8, 5),
            (-8, 6),
        ]
        self.rooms.add(Room(verts))


