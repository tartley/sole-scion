from math import pi
from random import randint, uniform

from pymunk import Vec2d
from shapely.geometry import Polygon

from solescion.geom.poly import irregular, regular
from solescion.model.chunk import Chunk
from solescion.model.material import rubber, ice, gold, granite, bamboo
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
        verts = [
            (15, 200), (-15, 200), (-100000, 201),
            (-100000, 200000), (100000, 200000), (100000, 201)]
        self.add_room(Room(verts))


    def select_branch_room(self):
        if len(self.rooms) == 1:
            room_idx = 0
        elif len(self.rooms) == 2:
            room_idx = 1
        else:
            room_idx = randint(2, len(self.rooms) - 1)
        return self.rooms.values()[room_idx]


    def _lowest_vert(self, room):
        lowest = 0
        for idx, vert in enumerate(room.verts):
            if vert[1] <= room.verts[lowest][1]:
                lowest = idx
        return lowest - 1


    def select_branch_wall(self, branch_room):
        if len(self.rooms) == 1:
            return 0
        elif len(self.rooms) % 2 == 0:
            return self._lowest_vert(branch_room)

        num_walls = len(branch_room.verts)
        if num_walls == len(branch_room.neighbours):
            return None
        while True:
            wall = randint(0, num_walls - 1)
            if wall not in branch_room.neighbours:
                return wall


    def new_room_verts(self, branch_room, branch_wall, num_verts):
        WALL_MIN = 10
        WALL_MAX = 50
        end = Vec2d(branch_room.verts[branch_wall])
        startidx = (branch_wall + 1) % len(branch_room.verts)
        start = Vec2d(branch_room.verts[startidx])
        gap = (start - end).get_length()
        room_radius = uniform(max(WALL_MIN, gap / 2), WALL_MAX)
        num_verts = int(max(4, 4 * room_radius / WALL_MIN / 2))
        verts = irregular(start, end, room_radius, num_verts)
        return verts


    def new_verts_ok(self, verts):
        if self.geometry is None:
            return True
        return self.geometry.touches(Polygon(verts))


    def add_room(self, newroom, branch_room=None, branch_wall=None):
        self.rooms[newroom.id] = newroom
        if branch_room is not None and branch_wall is not None:
            branch_room.attach(branch_wall, newroom, 0)
        if self.geometry is None:
            self.geometry = newroom.polygon
        else:
            self.geometry = self.geometry.union(newroom.polygon)


    # TODO untested
    def build(self, world, desired_size):
        self.create_initial_room()
        while len(self.rooms) < desired_size:
            branch_room = self.select_branch_room()
            branch_wall = self.select_branch_wall(branch_room)
            if branch_wall is None:
                continue
            num_verts = randint(4, 8)
            verts = self.new_room_verts(
                branch_room, branch_wall, num_verts)
            if self.new_verts_ok(verts):
                newroom = Room(verts)
                self.add_room(newroom, branch_room, branch_wall)
        world.rooms = self.rooms
        world.add_to_pymunk()

        for room in self.rooms.itervalues():
            self.furnish(room, world)


    chunkbits = [
        [
            Disc(rubber, 5),
        ],
        [
            Block(ice, [(-7, 4), (-6, 5), (5, 2), (2, -5)]),
        ],
        [
            Block(
                granite, [
                    (-5, 10), (-5, 15), (5, 20), (10, 15),
                    (10, 10), (5, 0), (0, 0)
                ]
            )
        ],
        [
            Block(gold, [(-9, 3), (9, 3), (9, -3), (-9, -3)]),
            Block(gold, [(-3, -9), (-3, 9), (3, 9), (3, -9)]),
        ],
        [
            Disc(bamboo, 5, (0, 0)),
            Disc(bamboo, 2, (0, 5)),
        ],
    ]

    # TODO: not tested
    def furnish(self, room, world):
        if 0 < room.id and room.id % 3 == 0:
            chunk_type = randint(0, len(self.chunkbits) - 1)
            chunk = Chunk(*self.chunkbits[chunk_type])
            world.add_chunk(chunk, room.centroid, uniform(0, 2*pi))

