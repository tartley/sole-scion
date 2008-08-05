#!/usr/bin/python -O

from math import pi

from pymunk import Body, Circle, moment_for_circle, Shape, Space

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.shapes.disc import Disc


class Disc_test(MyTestCase):

    def test_constructor(self):
        disc = Disc(5, 1, 2)

        self.assertEquals(disc.radius, 5, "didnt store radius")
        self.assertEquals(disc.x, 1, "didnt store x")
        self.assertEquals(disc.y, 2, "didnt store y")
        self.assertEquals(disc.mass, pi * 25, "disc mass wrong")
        expected = moment_for_circle(disc.mass, 0, 5, (1, 2))
        self.assertEquals(disc.moment, expected, "disc moment wrong")


    def test_add_to_space(self):
        space = Space()
        body = Body(1, 2)
        disc = Disc(5, 6, 7)

        disc.add_to_body(space, body)

        shape = space.shapes.pop()
        self.assertTrue(shape.body is body, "wrong body")
        self.assertEquals(type(shape), Circle, "wrong type")
        self.assertEquals(shape.radius, 5.0, "radius wrong")
        self.assertEquals(shape.center.x, 6.0, "offset wrong")
        self.assertEquals(shape.center.y, 7.0, "offset wrong")



if __name__ == "__main__":
    run_test(Disc_test)


