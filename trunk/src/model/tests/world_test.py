#!/usr/bin/python -O

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.entity import Entity
from model.world import World


class World_test(MyTestCase):

    def testConstructor(self):
        world = World()
        self.assertEquals(world.rooms, set(),
            "should have empty room collection")
        self.assertEquals(world.backColor, (0, 0, 255),
            "should set backcolor")


    def testPopulate(self):
        world = World()
        world.populate()
        self.assertEquals(len(world.rooms), 1, "should create one room")
        room = world.rooms.pop()
        self.assertEquals(len(room.verts), 5, "room should be a pentagon")
        self.assertEquals(room.color, (150, 100, 50),
            "room should be brown")


if __name__ == "__main__":
    run_test()
