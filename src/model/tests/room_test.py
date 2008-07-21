#!/usr/bin/python -O

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.room import Room


class Room_test(MyTestCase):

    def testConstructor(self):
        color = (0.1, 0.2, 0.3)
        verts = [(-1, -2), (3, 4), (-5, 6)]
        room = Room(color, verts)
        self.assertEquals(room.color, color, "should store color")
        self.assertEquals(room.verts, verts, "should store verts")


    def testConstructor_needs_at_least_three_vertices(self):
        expectedMsg = '__init__() takes exactly 3 arguments (1 given)'
        self.assertRaises(lambda: Room(), TypeError, expectedMsg)

        color = (0.5, 0.5, 0.5)
        expectedMsg = "need 3 or more verts"

        verts = []
        self.assertRaises(lambda: Room(color, verts), TypeError, expectedMsg)

        verts = [(0, 0)]
        self.assertRaises(lambda: Room(color, verts), TypeError, expectedMsg)

        verts = [(-1, 0), (1, 0)]
        self.assertRaises(lambda: Room(color, verts), TypeError, expectedMsg)


    def testConstructor_vertices_must_be_convex(self):
        self.fail("test not written")


    def testConstructor_needs_3_component_color(self):
        verts = [(-1, -2), (3, 4), (-5, 6)]

        color = object()
        expectedMsg = "object of type 'object' has no len()"
        self.assertRaises(lambda: Room(color, verts), TypeError, expectedMsg)

        color = ()
        expectedMsg = "bad color: ()"
        self.assertRaises(lambda: Room(color, verts), TypeError, expectedMsg)

        color = (1,)
        expectedMsg = "bad color: (1,)"
        self.assertRaises(lambda: Room(color, verts), TypeError, expectedMsg)

        color = (2, 3)
        expectedMsg = "bad color: (2, 3)"
        self.assertRaises(lambda: Room(color, verts), TypeError, expectedMsg)

        color = (3, 4, 5, 6)
        expectedMsg = "bad color: (3, 4, 5, 6)"
        self.assertRaises(lambda: Room(color, verts), TypeError, expectedMsg)


if __name__ == "__main__":
    run_test()
