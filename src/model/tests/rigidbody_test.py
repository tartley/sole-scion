#!/usr/bin/python -O

from __future__ import division
from math import pi

from pymunk import Body, Circle, moment_for_circle, Space, Vec2d

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.rigidbody import RigidBody
from model.shapes.block import Block
from model.shapes.disc import Disc


class MockShape(object):
    def __init__(self, mass, offset=None, moment=None):
        self.mass = mass
        self.offset = offset
        self.get_moment = lambda: moment


class RigidBody_test(MyTestCase):

    def test_constructor(self):
        body = RigidBody()
        self.assertNone(body.body, "bad body")
        self.assertEquals(body.shapes, (), "bad shapes")


    def test_constructor_adds_optional_shapes(self):
        orig = RigidBody.set_shapes
        RigidBody.set_shapes = Listener()
        try:
            shape1 = Disc(1)
            shape2 = Disc(2)
            shape3 = Disc(3)
            body = RigidBody(shape1, shape2, shape3)
            self.assertEquals(
                body.set_shapes.argsList,
                [(shape1, shape2, shape3),],
                "shapes not addded")
        finally:
            RigidBody.set_shapes = orig


    def test_position_read_from_body(self):
        body = RigidBody()
        self.assertNone(body.position, "bad initial position")
        self.assertNone(body.angle, "bad initial angle")

        space = Space()
        body.add_to_space(space, (11, 22), 0.456)
        self.assertEquals(body.position, Vec2d(11, 22), "bad position")
        self.assertAlmostEquals(body.angle, 0.456, places=7, msg="bad angle")


    def test_center_of_gravity(self):
        body0 = RigidBody()
        self.assertEquals(body0._center_of_gravity(), (0, 0), "bad COG0")

        shape1 = MockShape(2, offset=(10, 20))
        body = RigidBody()
        body.shapes = (shape1,)
        self.assertEquals(body._center_of_gravity(), (10, 20), "bad COG1")

        shape2 = MockShape(6, offset=(100, 50))
        body.shapes = (shape2,)
        self.assertEquals(body._center_of_gravity(), (100, 50), "bad COG2")

        body.shapes = (shape1, shape2)
        x = (600 + 20) / 8
        y = (300 + 40) / 8
        self.assertEquals(body._center_of_gravity(), (x, y), "bad COG3")


    def test_offset_shapes(self):
        body = RigidBody()
        sh1 = MockShape(None, offset=(10, 20))
        sh2 = MockShape(None, offset=(30, 40))
        body.shapes = [sh1, sh2]

        body._offset_shapes((+2, -3))

        self.assertEquals(body.shapes[0].offset, (8, 23), "bad sh1 offset")
        self.assertEquals(body.shapes[1].offset, (28, 43), "bad sh2 offset")


    def test_get_moment(self):
        body = RigidBody()
        self.assertEquals(body.get_moment(), 0.0, "bad initial moment")

        sh1 = MockShape(None, moment=5)
        sh2 = MockShape(None, moment=10)
        body.shapes = [sh1, sh2]

        self.assertEquals(body.get_moment(), 15.0, "bad moment")


    def test_get_mass(self):
        body = RigidBody()
        self.assertEquals(body.get_mass(), 0.0, "bad initial mass")

        sh1 = MockShape(5)
        sh2 = MockShape(10)
        body.shapes = [sh1, sh2]
        self.assertEquals(body.get_mass(), 15.0, "bad mass")


    def test_set_shapes_disc(self):
        radius = 4
        offset = (3, 2)
        disc = Disc(radius, offset)
        body = RigidBody()
        body.set_shapes(disc)

        self.assertEquals(body.shapes, (disc,), "bad shapes")
        shape = body.shapes[0]
        self.assertEquals(shape.offset, (0, 0))


    def test_set_shapes_block(self):
        verts = [(0, 0), (0, 1), (1, 1), (1, 0)]
        offset = (10, 20)
        block = Block(verts, offset)
        body = RigidBody()
        body.set_shapes(block)

        self.assertEquals(body.shapes, (block,), "bad shapes")
        shape = body.shapes[0]
        self.assertEquals(shape.offset, (0, 0), "bad offset")


    def test_set_shapes_two_discs(self):
        disc1 = Disc(4, (+100, +200))
        disc2 = Disc(2, (+115, +225))

        body = RigidBody()
        body.set_shapes(disc1, disc2)
        self.assertEquals(body.shapes, (disc1, disc2), "bad shapes")
        self.assertEquals(body.shapes[0].offset[0], -3.0, "bad offset1 x")
        self.assertAlmostEquals(body.shapes[0].offset[1], -5.0,
            msg="bad offset1 y")
        self.assertEquals(body.shapes[1].offset[0], +12.0, "bad offset2 x")
        self.assertAlmostEquals(body.shapes[1].offset[1], +20.0,
            msg="bad offset2 y")



    def test_add_to_space(self):
        disc1 = Disc(1)
        disc2 = Disc(2)
        disc3 = Disc(3)
        space = Space()
        body = RigidBody(disc1, disc2, disc3)

        body.add_to_space(space, (1, 2), 0.75)

        self.assertEquals(type(body.body), Body, "didnt create body")
        self.assertEquals(body.body.position, Vec2d(1, 2), "bad position")
        self.assertEquals(body.body.angle, 0.75, "bad angle")

        self.assertEquals(space.bodies, set([body.body]),
            "body not added to space")

        self.assertEquals(len(space.shapes), 3, "shapes not added to space")
        radii = set()
        for circle in space.shapes:
            self.assertEquals(circle.body, body.body, "bad Circle body")
            self.assertEquals(circle.friction, 0.5, "bad friction")
            self.assertEquals(circle.elasticity, 0.5, "bad elasticity")
            radii.add(circle.radius)
        self.assertEquals(radii, set([1, 2, 3]), "bad radii")


if __name__ == "__main__":
    run_test(RigidBody_test)

