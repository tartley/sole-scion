from model.room import Room

class World(object):

    def __init__(self):
        self.rooms = set()
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
        self.rooms.add(room)


