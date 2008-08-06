#!/usr/bin/python -O

from pymunk import Body, Circle, Space, Vec2d

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
        self.assertEquals((ent.x, ent.y), (2, 3), "didnt store position")
        self.assertEquals(ent.rot, 4.0, "didnt store rot")
        self.assertEquals(type(ent.body), Body, "didnt create body")


    def test_constructor_assigns_ids(self):
        disc = Disc(1, 0, 0)
        ent1 = Entity(disc, 0, 0, 0)
        self.assertEquals(type(ent1.entId), int,
            "should assign an integer entId")
        self.assertTrue(ent1.entId > 0, "should assign positive entId")

        ent2 = Entity(disc, 0, 0, 0)
        self.assertEquals(ent2.entId, ent1.entId + 1,
            "entIds should be sequential")


    def test_position_read_from_body(self):
        ent = Entity(Disc(1, 0, 0), 2, 3, 4)
        ent.body.position = (55, 66)
        ent.body.angle = 1.45
        self.assertEquals((ent.x, ent.y), (55, 66), "didnt use body position")
        self.assertAlmostEquals(ent.rot, 1.45, msg="didnt use body angle")


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
        self.assertEquals(ent.body, actualBody, "didnt store ents body")


if __name__ == "__main__":
    run_test(Entity_test)

