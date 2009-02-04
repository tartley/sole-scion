#!/usr/bin/python -O

import fixpath

from pymunk import Body, inf, Space

from solescion.testutils.listener import Listener
from solescion.testutils.testcase import MyTestCase, run

from solescion.geom.poly import centroid

from solescion.model.room import Room
from solescion.model.material import Material


class Room_test(MyTestCase):

    def test_constructor(self):
        color = (0.1, 0.2, 0.3)
        verts = [(-1, -2), (-5, 6), (3, 4)]
        Room._nextRoomId = 999
        room = Room(verts)
        self.assertEquals(room.id, 999, "should store id")
        self.assertEquals(Room._nextRoomId, 1000, "should inc next room id")
        self.assertEquals(room.material, Material.air, "bad material")
        self.assertEquals(room.verts, verts, "should store verts")
        self.assertEquals(room.neighbours, {}, 'bad neighbours')
        self.assertEquals(room.centroid, centroid(room.verts),
            'bad centroid')


    def test_constructor_validates_verts(self):
        listener = Listener()
        color = (0.1, 0.2, 0.3)
        verts = [(-1, -2), (3, 4), (-5, 6)]
        from solescion.model import room as room_module
        orig = room_module.assert_valid
        room_module.assert_valid = listener
        try:
            room = Room(verts)
        finally:
            room_module.assert_valid = orig
        self.assertEquals(listener.args, (verts,), "didnt validate verts")


    def test_attach(self):
        room1 = Room([(0, 0), (0, 1), (1, 1), (1, 0)])
        room2 = Room([(1, 0), (1, 1), (2, 1), (2, 0)])
        room1.attach(2, room2, 0)
        self.assertEquals(room1.neighbours, {2: room2})
        self.assertEquals(room2.neighbours, {0: room1})


    def test_add_to_body(self):
        color = (100, 150, 200)
        v1, v2, v3 = (0,1), (1,2), (2,0)
        verts = [v1, v2, v3]
        room = Room(verts)
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


    def test_add_to_body_should_not_add_segments_for_neighbours(self):
        color = (100, 150, 200)
        v1, v2, v3 = (0,1), (1,2), (2,0)
        verts = [v1, v2, v3]
        room = Room(verts)
        room.neighbours = {1: object(), 2: object()}
        space = Space()
        body = Body(inf, inf)

        room.add_to_body(space, body)

        segs = set([
            ((seg.a[0], seg.a[1]), (seg.b[0], seg.b[1]))
            for seg in space.static_shapes
        ])
        self.assertEquals(segs, set([(v1, v2)]),
            "wrong room walls added to space")

        for seg in space.static_shapes:
            self.assertEquals(seg.friction, 0.5, "bad wall friction")
            self.assertEquals(seg.elasticity, 0.5, "bad wall elasticity")


if __name__ == "__main__":
    run(Room_test)

