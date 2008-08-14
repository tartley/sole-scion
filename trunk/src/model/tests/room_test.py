#!/usr/bin/python -O

from pyglet.window import Window
from pymunk import Body, inf, Space

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.room import Room


class Room_test(MyTestCase):

    def test_constructor(self):
        color = (0.1, 0.2, 0.3)
        verts = [(-1, -2), (-5, 6), (3, 4)]
        room = Room(color, verts)
        self.assertEquals(room.color, color, "should store color")
        self.assertEquals(room.verts, verts, "should store verts")


    def test_constructor_validates_verts(self):
        listener = Listener()
        color = (0.1, 0.2, 0.3)
        verts = [(-1, -2), (3, 4), (-5, 6)]
        from model import room as room_module
        orig = room_module.assert_valid_poly
        room_module.assert_valid_poly = listener
        try:
            room = Room(color, verts)
        finally:
            room_module.assert_valid_poly = orig
        self.assertEquals(listener.args, (verts,), "didnt validate verts")


    def test_add_to_body(self):
        color = (100, 150, 200)
        v1, v2, v3 = (0,1), (1,2), (2,0)
        verts = [v1, v2, v3]
        room = Room(color, verts)
        space = Space()
        body = Body(inf, inf)

        room.add_to_body(space, body)

        segs = set([
            ((seg.a[0], seg.a[1]), (seg.b[0], seg.b[1]))
            for seg in space.static_shapes
        ])
        self.assertEquals(segs, set([(v1, v2), (v2, v3), (v3, v1)]),
            "room walls not added to space")

        for seg in space.static_shapes:
            self.assertEquals(seg.friction, 0.5, "bad wall friction")
            self.assertEquals(seg.elasticity, 0.5, "bad wall elasticity")


if __name__ == "__main__":
    run_test(Room_test)