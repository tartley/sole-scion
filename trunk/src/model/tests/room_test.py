#!/usr/bin/python -O

from pymunk import Body, inf, Space

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.room import Room


class Room_test(MyTestCase):

    def test_constructor(self):
        color = (0.1, 0.2, 0.3)
        verts = [(-1, -2), (3, 4), (-5, 6)]
        room = Room(color, verts)
        self.assertEquals(room.color, color, "should store color")
        self.assertEquals(room.verts, verts, "should store verts")


    def test_constructor_rejects_less_than_three_vertices(self):
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


    def test_constructor_rejects_nonconvex_vertices(self):
        self.fail("not tested")


    def test_constructor_rejects_bad_color(self):
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


    def test_add_to(self):
        color = (100, 150, 200)
        v1, v2, v3 = (0,1), (2,3), (4,5)
        verts = [v1, v2, v3]
        room = Room(color, verts)
        space = Space()
        body = Body(inf, inf)

        room.add_to(space, body)

        segs = set([
            ((seg.a[0], seg.a[1]), (seg.b[0], seg.b[1]))
            for seg in space.static_shapes
        ])
        self.assertEquals(segs, set([(v1, v2), (v2, v3), (v3, v1)]),
            "room walls not added to space")


if __name__ == "__main__":
    run_test(Room_test)
