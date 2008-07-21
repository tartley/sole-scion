from model.room import Room

class World(object):

    def __init__(self):
        self.rooms = set()
        self.backColor = (0.0, 0.0, 1.0, 1.0)


    def populate(self):
        color = (0.1, 0.2, 0.3)
        verts = [
            (-10, 0),
            (0, -1),
            (+10, 1),
            (+8, 5),
            (-8, 6),
        ]
        self.rooms.add(Room(color, verts))


