#!/usr/bin/python -O

from pymunk import Body, inf, Space

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.entity import Entity
from model.room import Room
from model.world import World


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
        v1, v2, v3 = (0, 0), (100, 0), (0, 100)
        verts = [v1, v2, v3]
        room = Room(color, verts)
        room.add_to = Listener()

        world.add_room(room)

        self.assertEquals(world.rooms, set([room]), "room not added")
        self.assertEquals(room.add_to.args, (world.space, world.staticBody),
            "room walls not added to space")


    def test_add_entity(self):
        world = World()
        entity = Entity()
        entity.add_to = Listener()

        world.add_entity(entity)

        self.assertEquals(world.entities, set([entity]), "ent not added")
        self.assertEquals(entity.add_to.args, (world.space,),
            "ent not added to space")


if __name__ == "__main__":
    run_test(World_test)
