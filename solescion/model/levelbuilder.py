from math import cos, sin, pi
from random import randint

from solescion.geom.poly import create_regular
from solescion.model.room import Room


class LevelBuilder(object):

    def __init__(self):
        self.rooms = {}


    def create_initial_room(self):
        verts = create_regular(randint(3, 8), (+20, -30), (-20, -30))
        room = Room(verts)
        self.rooms = {room.id: room}


    def select_branch_room(self):
        return self.rooms.values()[randint(0, len(self.rooms) - 1)]


    def select_branch_wall(self, branch_room):
        if len(branch_room.verts) == len(branch_room.neighbours):
            return None
        while True:
            wall = randint(0, len(branch_room.verts) - 1)
            if wall not in branch_room.neighbours:
                return wall


    def new_room_verts(self, branch_room, branch_wall, num_verts):
        end = branch_room.verts[branch_wall]
        startidx = (branch_wall + 1) % len(branch_room.verts)
        start = branch_room.verts[startidx]
        verts = create_regular(num_verts, start, end)
        return verts


    def new_verts_ok(self, _):
        return True


    def add_new_room(self, newroom, branch_room, branch_wall):
        self.rooms[newroom.id] = newroom
        branch_room.attach(branch_wall, newroom, 0)


    def add_to_world(self, world):
        for room in self.rooms.itervalues():
            world.add_room(room)


    # TODO untested
    def build(self, world):
        from random import seed
        seed(1)
        self.create_initial_room()
        for _ in xrange(5):
            while True:
                branch_room = self.select_branch_room()
                branch_wall = self.select_branch_wall(branch_room)
                if branch_wall is None:
                    continue
                num_verts = randint(3, 8)
                verts = self.new_room_verts(
                    branch_room, branch_wall, num_verts)
                if self.new_verts_ok(verts):
                    break
            self.add_new_room(Room(verts), branch_room, branch_wall)
        self.add_to_world(world)

