#!/usr/bin/python -O

from math import pi

from pymunk import Body, Circle, moment_for_circle, Shape, Space, Vec2d

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.shapes.disc import Disc


class Disc_test(MyTestCase):

    def test_constructor(self):
        radius = 5
        offset = (1, 2)
        disc = Disc(radius, offset)

        self.assertEquals(disc.radius, 5, "didnt store radius")
        self.assertEquals(disc.offset, (1, 2), "didnt store offset")
        self.assertEquals(disc.mass, pi * 25, "mass wrong")
        self.assertNone(disc.shape, "shape wrong")
        self.assertValidColor(disc.color)


    def test_constructor_offset_defaults_to_zero(self):
        disc = Disc(5)
        self.assertEquals(disc.offset, (0, 0), "bad offset")


    def test_get_moment(self):
        radius = 5
        offset = (1, 2)
        disc = Disc(radius, offset)
        expected = moment_for_circle(disc.mass, 0, radius, offset)
        self.assertEquals(disc.get_moment(), expected, "bad moment")


    def test_add_to_body(self):
        disc = Disc(5, (1, 2))
        body = Body(0, 0)
        space = Space()
        space.add(body)

        disc.add_to_body(space, body)

        self.assertNotNone(disc.shape, "didnt create shape")
        self.assertEquals(disc.shape.body, body, "didnt add shape to body")
        self.assertEquals(disc.shape.radius, 5.0, "bad radius")
        self.assertEquals(disc.shape.center, Vec2d(1.0, 2.0), "bad center")
        self.assertEquals(disc.shape.friction, 0.5, "bad friction")
        self.assertEquals(disc.shape.elasticity, 0.5, "bad elasticity")
        self.assertEquals(space.shapes, [disc.shape],
            "didn't add shape to space")


if __name__ == "__main__":
    run_test(Disc_test)


