#!/usr/bin/python -O

from pymunk import Body, inf, Space, Vec2d

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.chunk import Chunk
from model.material import gold
from model.room import Room
from model.world import World
from model.shards.disc import Disc


class World_test(MyTestCase):

    def test_constructor(self):
        from model import world as world_module
        orig = world_module.init_pymunk
        world_module.init_pymunk = Listener()
        try:
            world = World()

            self.assertTrue(world_module.init_pymunk.triggered,
                "should init_pymunk")
        finally:
            world_module.init_pymunk = orig

        self.assertEquals(type(world.space), Space, "should create a Space")
        self.assertEquals(world.space.gravity, Vec2d(0, -10),
            "should set gravity")
        self.assertEquals(type(world.staticBody), Body, "should create a body")
        self.assertEquals(world.rooms, set(), "should create empty room set")
        self.assertEquals(world.backColor, (150, 100, 50),
            "should set backcolor")


    def test_populate(self):
        world = World()
        world.add_room = Listener()

        world.populate()

        self.assertEquals(world.add_room.triggerCount, 1, "should add 1 room")
        room = world.add_room.args[0]
        self.assertEquals(len(room.verts), 5, "room should be a pentagon")
        self.assertEquals(room.color, (0, 50, 100),
            "room should be brown")


    def test_add_room(self):
        world = World()
        color = (50, 100, 200)
        v1, v2, v3 = (0, 0), (0, 100), (100, 0)
        verts = [v1, v2, v3]
        room = Room(color, verts)
        room.add_to_body = Listener()

        world.add_room(room)

        self.assertEquals(world.rooms, set([room]), "room not added")
        expected = (world.space, world.staticBody)
        self.assertEquals(room.add_to_body.args, expected,
            "room walls not added to space")


    def test_add_chunk(self):
        world = World()
        chunk = Chunk(Disc(gold, 1))
        chunk.add_to_space = Listener()

        world.add_chunk(chunk, (1, 2), 0.5)

        self.assertEquals(world.rigidBodies, set([chunk]),
            "chunk not added")
        self.assertEquals(
            chunk.add_to_space.args,
            (world.space, (1, 2), 0.5),
            "chunk not added to space")


    def test_add_chunk_default_angle(self):
        world = World()
        rigidBody = Chunk(Disc(gold, 1))

        world.add_chunk(rigidBody, (10, 20))

        body = [b for b in world.space.bodies][0]
        self.assertEquals(body.angle, 0.0, "bad default angle")


    def test_tick(self):
        world = World()
        world.space.step = Listener()

        world.tick(1/42)

        self.assertEquals(world.space.step.args, (1/42,), "didn't step")


if __name__ == "__main__":
    run_test(World_test)
