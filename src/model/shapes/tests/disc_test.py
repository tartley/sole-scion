#!/usr/bin/python -O

from math import pi

from pymunk import Body, Circle, moment_for_circle, Shape, Space, Vec2d

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.shapes.disc import Disc


class Disc_test(MyTestCase):

    def test_constructor(self):
        disc = Disc(1, 2, 5)

        self.assertEquals(disc.radius, 5, "didnt store radius")
        self.assertEquals(disc.offset, (1, 2), "didnt store offset")
        self.assertEquals(disc.mass, pi * 25, "mass wrong")
        expected = moment_for_circle(disc.mass, 0, 5, (1, 2))
        self.assertEquals(disc.moment, expected, "moment wrong")
        self.assertNone(disc.shape, "shape wrong")


    def test_add_to_body(self):
        disc = Disc(1, 2, 5)
        space = Space()
        body = Body(10, 20)

        disc.add_to_body(space, body)

        self.assertEquals(type(disc.shape), Circle, "didnt create shape")
        self.assertEquals(disc.shape.body, body, "didnt add shape to body")
        self.assertEquals(disc.shape.radius, 5.0, "bad radius")
        self.assertEquals(disc.shape.center, Vec2d(1.0, 2.0), "bad offset")
        self.assertEquals(disc.shape.friction, 0.5, "bad friction")
        self.assertEquals(disc.shape.elasticity, 0.5, "bad elasticity")
        spaceShape = space.shapes.pop()
        self.assertEquals(disc.shape, spaceShape, "didn't add shape to space")


if __name__ == "__main__":
    run_test(Disc_test)


