#!/usr/bin/python -O

from __future__ import division
from math import pi

from pymunk import Body, Circle, moment_for_circle, Space, Vec2d

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.rigidbody import RigidBody
from model.shapes.disc import Disc


class MockShape(object):
    def __init__(self, mass, offset=None, moment=None):
        self.mass = mass
        self.offset = offset
        self.get_moment = lambda: moment


class RigidBody_test(MyTestCase):

    def test_constructor(self):
        body = RigidBody()
        self.assertEquals(type(body.body), Body, "didnt create body")
        self.assertEquals(body.body.mass, 0.0, "bad mass")
        self.assertEquals(body.body.moment, 0.0, "bad moment")
        self.assertEquals(body.body.position, Vec2d(0.0, 0.0), "bad position")
        self.assertEquals(body.body.angle, 0.0, "bad angle")
        self.assertEquals(body.shapes, [], "bad shapes")


    def test_constructor_takes_optional_shapes(self):
        body = RigidBody()
        body.add_shape = Listener()
        sh1 = Disc(1)
        sh2 = Disc(2)
        sh3 = Disc(3)
        body.__init__(sh1, sh2, sh3)
        self.assertEquals(body.add_shape.argsList, [(sh1,), (sh2,), (sh3,)],
            "shapes not addded")


    def test_position_read_from_body(self):
        body = RigidBody()
        body.body.position = (55, 66)
        body.body.angle = 1.45
        self.assertEquals(body.position, Vec2d(55, 66),
            "didnt use body position")
        self.assertAlmostEquals(body.angle, 1.45, msg="didnt use body angle")


    def test_center_of_gravity(self):
        body = RigidBody()

        obj1 = MockShape(2, offset=(10, 20))
        body.shapes.append(obj1)
        body.body.mass += obj1.mass
        self.assertEquals(body._center_of_gravity(), (10, 20), "bad COG1")

        obj2 = MockShape(6, offset=(100, 50))
        body.shapes.append(obj2)
        body.body.mass += obj2.mass
        x = (600 + 20) / 8
        y = (300 + 40) / 8
        self.assertEquals(body._center_of_gravity(), (x, y), "bad COG2")


    def test_offset_position(self):
        body = RigidBody()
        body.body.position = (100, 200)
        sh1 = MockShape(None, offset=(10, 20))
        sh2 = MockShape(None, offset=(30, 40))
        body.shapes = [sh1, sh2]

        body._offset_position((+2, -3))

        self.assertEquals(body.body.position, Vec2d(102, 197),
            "bad body position")
        self.assertEquals(body.shapes[0].offset, (8, 23), "bad sh1 offset")
        self.assertEquals(body.shapes[1].offset, (28, 43), "bad sh2 offset")


    def test_get_moment(self):
        body = RigidBody()
        sh1 = MockShape(None, moment=5)
        sh2 = MockShape(None, moment=10)
        body.shapes = [sh1, sh2]

        self.assertEquals(body.get_moment(), 15.0, "bad moment")


    def test_add_shape_disc(self):
        radius = 4
        offset = (3, 2)
        disc = Disc(radius, offset)

        body = RigidBody()
        body.add_shape(disc)

        expectedMass = pi * radius * radius
        self.assertAlmostEquals(body.body.mass, expectedMass, places=5,
            msg="bad mass")
        expectedMoment = moment_for_circle(expectedMass, 0, radius, (0, 0))
        self.assertEquals(body.body.moment, expectedMoment, "bad moment")
        self.assertEquals(body.body.position, Vec2d(3, 2), "bad position")

        self.assertEquals(body.shapes, [disc], "bad shapes")


    def test_add_to_space(self):
        disc1 = Disc(1)
        disc2 = Disc(2)
        disc3 = Disc(3)
        body = RigidBody(disc1, disc2, disc3)
        space = Space()

        body.add_to_space(space, (1, 2), 0.75)

        self.assertEquals(body.body.position, Vec2d(1, 2), "bad position")
        self.assertEquals(body.body.angle, 0.75, "bad angle")

        self.assertEquals(space.bodies, set([body.body]),
            "body not added to space")

        radii = set()
        for circle in space.shapes:
            self.assertEquals(circle.body, body.body, "bad Circle body")
            self.assertEquals(circle.friction, 0.5, "bad friction")
            self.assertEquals(circle.elasticity, 0.5, "bad elasticity")
            radii.add(circle.radius)
        self.assertEquals(radii, set([1, 2, 3]), "bad radii")


if __name__ == "__main__":
    run_test(RigidBody_test)

