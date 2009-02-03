#!/usr/bin/python -O

import fixpath

from pymunk import Body, inf, Space, Vec2d

from solescion.testutils.listener import Listener
from solescion.testutils.testcase import MyTestCase, run

from solescion.model.chunk import Chunk
from solescion.model.material import Material
from solescion.model.room import Room
from solescion.model.world import World
from solescion.model.shards.disc import Disc


class World_test(MyTestCase):

    def test_constructor(self):
        world = World()
        self.assertEquals(type(world.space), Space,
            "should create a Space")
        self.assertEquals(world.space.gravity, Vec2d(0, -10),
            "should set gravity")
        self.assertEquals(
            world.space._space.contents.elasticIterations, 10,
            "should set elasticIterations")
        self.assertEquals(type(world.static_body), Body,
            "should create a body")
        self.assertEquals(world.rooms, {},
            "should create empty room set")
        self.assertEquals(world.material, Material.granite, "bad material")


    def test_constructor_initialises_pymunk(self):
        from solescion.model import world as world_module
        orig = world_module.init_pymunk
        world_module.init_pymunk = Listener()
        try:
            world = World()
            self.assertTrue(world_module.init_pymunk.triggered,
                "should init_pymunk")
        finally:
            world_module.init_pymunk = orig


    def test_add_room(self):
        world = World()
        color = (50, 100, 200)
        v1, v2, v3 = (0, 0), (0, 100), (100, 0)
        verts = [v1, v2, v3]
        room = Room(verts)
        room.id = 9876
        room.add_to_body = Listener()

        world.add_room(room)

        self.assertEquals(world.rooms, {room.id: room}, "room not added")
        expected = (world.space, world.static_body)
        self.assertEquals(room.add_to_body.args, expected,
            "room walls not added to space")


    def test_add_chunk(self):
        world = World()
        chunk = Chunk(Disc(Material.gold, 1))
        chunk.add_to_space = Listener()

        world.add_chunk(chunk, (1, 2), 0.5)

        self.assertEquals(world.chunks, set([chunk]), "chunk not added")
        self.assertEquals(
            chunk.add_to_space.args,
            (world.space, (1, 2), 0.5),
            "chunk not added to space")


    def test_add_chunk_default_angle(self):
        world = World()
        chunk = Chunk(Disc(Material.gold, 1))

        world.add_chunk(chunk, (10, 20))

        body = [b for b in world.space.bodies][0]
        self.assertEquals(body.angle, 0.0, "bad default angle")


    def test_tick(self):
        world = World()
        world.space.step = Listener()
        class Mock(object):
            pass
        world.player = Mock()
        world.player.move = lambda *_: None

        world.tick(1/42)

        self.assertEquals(world.space.step.args, (1/42,), "didn't step")


if __name__ == "__main__":
    run(World_test)
