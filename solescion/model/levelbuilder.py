from random import randint, seed

from shapely.geometry import Polygon

from solescion.geom.poly import regular
from solescion.model.chunk import Chunk
from solescion.model.material import Material
from solescion.model.room import Room
from solescion.model.shards.block import Block
from solescion.model.shards.disc import Disc


class LevelBuilder(object):
    # pylint: disable-msg=R0201
    #   Method could be a function: acknowledged.

    def __init__(self):
        self.rooms = {}
        self.geometry = None


    def create_initial_room(self):
        verts = regular(7, (+20, -30), (-20, -30))
        self.add_room(Room(verts))


    def complete(self):
        return len(self.rooms) > 88


    def select_branch_room(self):
        return self.rooms.values()[len(self.rooms) - 1]


    def select_branch_wall(self, branch_room):
        num_walls = len(branch_room.verts)
        if num_walls == len(branch_room.neighbours):
            return None
        while True:
            wall = randint(0, num_walls - 1)
            if wall not in branch_room.neighbours:
                return wall


    def new_room_verts(self, branch_room, branch_wall, num_verts):
        end = branch_room.verts[branch_wall]
        startidx = (branch_wall + 1) % len(branch_room.verts)
        start = branch_room.verts[startidx]
        verts = regular(num_verts, start, end)
        return verts


    def new_verts_ok(self, verts):
        if self.geometry is None:
            return True
        return self.geometry.touches(Polygon(verts))


    def add_room(self, newroom, branch_room=None, branch_wall=None):
        self.rooms[newroom.id] = newroom
        if branch_room and branch_wall:
            branch_room.attach(branch_wall, newroom, 0)
        if self.geometry is None:
            self.geometry = newroom.polygon
        else:
            self.geometry = self.geometry.union(newroom.polygon)


    # TODO untested
    def build(self, world):
        seed(2)
        self.create_initial_room()
        while not self.complete():
            branch_room = self.select_branch_room()
            branch_wall = self.select_branch_wall(branch_room)
            if branch_wall is None:
                continue
            num_verts = randint(3, 8)
            verts = self.new_room_verts(
                branch_room, branch_wall, num_verts)
            if self.new_verts_ok(verts):
                self.add_room(Room(verts), branch_room, branch_wall)

        world.rooms = self.rooms
        world.add_to_pymunk()

        for room in self.rooms.itervalues():
            self.furnish(room, world)


    chunkbits = [
        [
            Disc(Material.rubber, 5),
        ],
        [
            Block(Material.ice, [(-10, 5), (5, 2), (2, 0), (0, 0)]),
        ],
        [
            Block(
                Material.granite, [
                    (-5, 10), (-5, 15), (5, 20), (10, 15),
                    (10, 10), (5, 0), (0, 0)
                ]
            )
        ],
        [
            Block(Material.gold, [(-9, 3), (9, 3), (9, -3), (-9, -3)]),
            Block(Material.gold, [(-3, -9), (-3, 9), (3, 9), (3, -9)]),
        ],
        [
            Disc(Material.bamboo, 5, (0, -2)),
            Disc(Material.bamboo, 2, (0, 0)),
        ],
    ]

    # TODO: not tested
    def furnish(self, room, world):
        if room.id > 0:
            chunk = Chunk(*self.chunkbits[randint(0, len(self.chunkbits) - 1)])
            world.add_chunk(chunk, room.centroid)

