#!/usr/bin/python -O

from math import pi

import fixpath

from pymunk import (
    Body, Circle, moment_for_circle, Shape, Space, Vec2d,
)

from solescion.testutils.testcase import MyTestCase, run

from solescion.model.shards.disc import Disc
from solescion.model.material import gold


class Disc_test(MyTestCase):

    def test_constructor(self):
        radius = 5
        offset = (1, 2)
        disc = Disc(gold, radius, offset)

        self.assertEquals(disc.material, gold, "didnt store color")
        self.assertEquals(disc.radius, 5, "didnt store radius")
        self.assertEquals(disc.center, (1, 2), "didnt store offset")
        self.assertAlmostEquals(disc.mass, gold.density * pi * 25,
            msg="mass wrong")
        self.assertNone(disc.shape, "shape wrong")


    def test_constructor_offset_defaults_to_zero(self):
        disc = Disc(gold, 5)
        self.assertEquals(disc.center, (0, 0), "bad center")


    def test_get_moment(self):
        radius = 5
        offset = (1, 2)
        disc = Disc(gold, radius, offset)
        expected = moment_for_circle(disc.mass, 0, radius, offset)
        self.assertEquals(disc.get_moment(), expected, "bad moment")


    def test_get_centroid(self):
        disc = Disc(gold, 10, (111, 222))
        self.assertEquals(disc.get_centroid(), (111, 222), "bad offset")


    def test_offset(self):
        disc = Disc(gold, 10, (11, 22))
        disc.offset((100, 200))
        self.assertEquals(disc.get_centroid(), (111, 222), "didnt apply offset")


    def test_add_to_body(self):
        disc = Disc(gold, 5, (1, 2))
        body = Body(0, 0)
        space = Space()
        space.add(body)

        disc.add_to_body(space, body)

        self.assertNotNone(disc.shape, "didnt create shape")
        self.assertEquals(disc.shape.body, body, "didnt add shape to body")
        self.assertEquals(disc.shape.radius, 5.0, "bad radius")
        self.assertEquals(disc.shape.center, Vec2d(1.0, 2.0), "bad center")
        self.assertAlmostEquals(disc.shape.friction, gold.friction,
            msg="bad friction")
        self.assertAlmostEquals(disc.shape.elasticity, gold.elasticity,
            msg="bad elasticity")
        self.assertEquals(space.shapes, [disc.shape],
            "didn't add shape to space")


if __name__ == "__main__":
    run(Disc_test)

