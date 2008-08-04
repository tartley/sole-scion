#!/usr/bin/python -O
from pymunk import Body, Circle, Space

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.entity import Entity


class Entity_test(MyTestCase):

    def test_constructor_assigns_ids(self):
        ent1 = Entity()
        self.assertEquals(type(ent1.entId), int,
            "should assign an integer entId")
        self.assertTrue(ent1.entId > 0, "should assign positive entId")

        ent2 = Entity()
        self.assertEquals(ent2.entId, ent1.entId + 1,
            "entId should be unique and sequential")


    def test_add_to(self):
        ent = Entity()
        space = Space()

        ent.add_to(space)

        self.assertEquals(len(space.bodies), 1, "ent body not added to space")
        body = space.bodies.pop()
        self.assertEquals(body.mass, 1.0, "mass wrong")
        self.assertEquals(body.moment, 1.0, "moment wrong")

        self.assertEquals(len(space.shapes), 1, "ent shape not added to space")
        shape = space.shapes.pop()
        self.assertEquals(type(shape), Circle, "shape type wrong")
        self.assertEquals(shape.radius, 1.0, "shape radius wrong")



if __name__ == "__main__":
    run_test(Entity_test)
