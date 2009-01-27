#!/usr/bin/python -O

from random import seed
from math import sqrt

import fixpath

from solescion.testutils.listener import Listener
from solescion.testutils.testcase import MyTestCase, run

from solescion.model.levelbuilder import LevelBuilder
from solescion.model.room import Room


class LevelBuilder_test(MyTestCase):

    def setUp(self):
        seed(0)


    def test_constructor(self):
        builder = LevelBuilder()
        self.assertEquals(builder.rooms, {})


    def test_create_initial_room(self):
        builder = LevelBuilder()
        builder.create_initial_room()
        self.assertEquals(builder.rooms.keys(), [0])
        self.assertTrue(isinstance(builder.rooms[0], Room))


    def test_select_branch_room(self):
        builder = LevelBuilder()
        r1, r2, r3 = object(), object(), object()
        builder.rooms = {1: r1, 11: r2, 111: r3}
        selected = set()

        for _ in xrange(32):
            selected.add(builder.select_branch_room())

        self.assertEquals(selected, set([r1, r2, r3]))


    def test_select_branch_wall_no_free_walls(self):
        builder = LevelBuilder()
        room = Listener()
        room.verts = range(3)
        room.neighbours = range(3)
        self.assertNone(builder.select_branch_wall(room))


    def test_select_branch_wall(self):
        builder = LevelBuilder()
        room = Listener()
        room.verts = range(5)
        room.neighbours = {0: object(), 2:object(), 3:object()}
        walls = set()

        for _ in xrange(32):
            walls.add(builder.select_branch_wall(room))

        self.assertEquals(walls, set([1, 4]))


    def test_new_room_verts(self):
        builder = LevelBuilder()
        room = Listener()
        room.verts = [(1, 11), (2, 22), (3, 33), (4, 44)]
        wall = 1
        for num_verts in xrange(3, 5):

            verts = builder.new_room_verts(room, wall, num_verts)

            self.assertEquals(len(verts), num_verts)
            self.assertEquals(verts[0], (3, 33))
            self.assertEquals(verts[1], (2, 22))


    def test_new_room_verts_tri_on_final_wall(self):
        builder = LevelBuilder()
        room = Listener()
        room.verts = [(1, 11), (2, 22), (3, 33), (4, 44)]
        wall = 3

        verts = builder.new_room_verts(room, wall, 3)

        self.assertEquals(len(verts), 3)
        self.assertEquals(verts[0], (1, 11))
        self.assertEquals(verts[1], (4, 44))


    def test_new_verts_ok(self):
        builder = LevelBuilder()
        self.assertEquals(builder.new_verts_ok(None), True)


    def test_create_new_room(self):
        builder = LevelBuilder()
        branch_room = Room([(1, 0), (0, 0), (0, 1)])
        branch_wall = 5
        room = Room([(1, 0), (0, 0), (0, 1)])
        room.neighbours = {}

        builder.add_new_room(room, branch_room, branch_wall)

        self.assertEquals(len(builder.rooms), 1)
        new_room = builder.rooms.values()[0]
        self.assertEquals(new_room.neighbours, {0: branch_room})
        self.assertEquals(branch_room.neighbours, {branch_wall: new_room})

    def test_add_to_world(self):
        world = Listener()
        world.add_room = Listener()
        builder = LevelBuilder()
        r1, r2, r3 = object(), object(), object()
        builder.rooms = {100: r1, 200: r2, 300: r3}
        builder.add_to_world(world)
        self.assertEquals(
            set(world.add_room.args_list),
            set([(r1,), (r2,), (r3,)]))


if __name__ == "__main__":
    run(LevelBuilder_test)

