#!/usr/bin/python -O
from pymunk import Body, Circle, Space

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.entity import Entity
from model.shapes.disc import Disc


class Entity_test(MyTestCase):

    def test_constructor(self):
        disc = Disc(1, 0, 0)
        ent = Entity(disc, 2, 3, 4)
        self.assertEquals(ent.shape, disc, "didnt store shapes")
        self.assertEquals(ent.x, 2, "didnt store x")
        self.assertEquals(ent.y, 3, "didnt store y")
        self.assertEquals(ent.rot, 4, "didnt store rot")


    def test_constructor_assigns_ids(self):
        disc = Disc(1, 0, 0)
        ent1 = Entity(disc, 0, 0, 0)
        self.assertEquals(type(ent1.entId), int,
            "should assign an integer entId")
        self.assertTrue(ent1.entId > 0, "should assign positive entId")

        ent2 = Entity(disc, 0, 0, 0)
        self.assertEquals(ent2.entId, ent1.entId + 1,
            "entIds should be sequential")


    def test_add_to_space(self):
        disc = Disc(1, 0, 0)
        disc.add_to_body = Listener()
        ent = Entity(disc, 1, 2, 3)
        space = Space()

        ent.add_to_space(space)

        actualSpace, actualBody = disc.add_to_body.args
        self.assertEquals(actualSpace, space, "shape not added to space")
        self.assertEquals(type(actualBody), Body, "shape not added to a body")
        self.assertEquals(space.bodies.pop(), actualBody,
            "body not added to space")


if __name__ == "__main__":
    run_test(Entity_test)

