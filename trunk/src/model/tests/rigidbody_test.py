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


class RigidBody_test(MyTestCase):

    def setUp(self):
        self.unitsquare = [(0, 0), (0, 1), (1, 1), (1, 0)]


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

        shape1 = Disc(2, (10, 20))
        body = RigidBody()
        body.shapes = (shape1,)
        self.assertEquals(body._center_of_gravity(), (10, 20), "bad COG1")

        verts = [(99, 49), (99, 51), (101, 51), (101, 49)]
        shape2 = Block(verts)
        body.shapes = (shape2,)
        self.assertEquals(body._center_of_gravity(), (100, 50), "bad COG2")

        body.shapes = (shape1, shape2)
        totalMass = shape1.mass + shape2.mass
        x = (10 * 4*pi + 100 * 4) / totalMass
        y = (20 * 4*pi + 50 * 4) / totalMass
        self.assertEquals(body._center_of_gravity(), (x, y), "bad COG3")


    def test_offset_shapes(self):
        body = RigidBody()
        sh1 = Disc(5, (10, 20))
        sh2 = Block(self.unitsquare, (30, 40), center=True)
        body.shapes = [sh1, sh2]

        body._offset_shapes((+2, -3))

        offset1 = body.shapes[0].get_offset()
        self.assertEquals(offset1, (12, 17), "bad sh1 offset")
        offset2 = body.shapes[1].get_offset() 
        self.assertEquals(offset2, (32, 37), "bad sh2 offset")


    def test_get_moment(self):
        body = RigidBody()
        self.assertEquals(body.get_moment(), 0.0, "bad initial moment")

        sh1 = Disc(2, (10, 20))
        sh2 = Block(self.unitsquare, (100, 200))
        body.shapes = [sh1, sh2]

        expected = sh1.get_moment() + sh2.get_moment()
        self.assertEquals(body.get_moment(), expected, "bad moment")


    def test_get_mass(self):
        body = RigidBody()
        self.assertEquals(body.get_mass(), 0.0, "bad initial mass")

        sh1 = Disc(5)
        sh2 = Block(self.unitsquare)
        body.shapes = [sh1, sh2]
        self.assertEquals(body.get_mass(), 25*pi + 1, "bad mass")


    def test_set_shapes_disc(self):
        radius = 4
        offset = (3, 2)
        disc = Disc(radius, offset)
        body = RigidBody()
        body.set_shapes(disc)

        self.assertEquals(body.shapes, (disc,), "bad shapes")
        shape = body.shapes[0]
        self.assertEquals(shape.get_offset(), (0, 0))


    def test_set_shapes_two_discs(self):
        disc1 = Disc(4, (+100, +200))
        disc2 = Disc(2, (+115, +225))

        body = RigidBody()
        body.set_shapes(disc1, disc2)
        self.assertEquals(body.shapes, (disc1, disc2), "bad shapes")
        shape1offset = body.shapes[0].get_offset()
        self.assertEquals(shape1offset[0], -3.0, "bad offset1 x")
        self.assertAlmostEquals(shape1offset[1], -5.0,
            msg="bad offset1 y")
        shape2offset = body.shapes[1].get_offset()
        self.assertEquals(shape2offset[0], +12.0, "bad offset2 x")
        self.assertAlmostEquals(shape2offset[1], +20.0,
            msg="bad offset2 y")


    def test_set_shapes_block(self):
        verts = [(0, 0), (0, 1), (1, 1), (1, 0)]
        offset = (10, 20)
        block = Block(verts, offset)
        self.assertEquals(block.get_offset(), (10.5, 20.5), "bad offset")

        body = RigidBody()
        body.set_shapes(block)

        self.assertEquals(body.shapes, (block,), "bad shapes")
        shape = body.shapes[0]
        self.assertEquals(shape.get_offset(), (0, 0), "bad offset")


    def test_set_shapes_two_blocks(self):
        verts1 = [(0, 0), (0, 4), (4, 4), (4, 0)]
        block1 = Block(verts1, (8, 0))
        verts2 = [(0, 0), (0, 4), (12, 4), (12, 0)]
        block2 = Block(verts2, (0, 4))
        body = RigidBody(block1, block2)

        self.assertEquals(body.shapes, (block1, block2,), "shapes not added")
        self.assertEquals(block1.get_offset(), (+3, -3), "bad offset1")
        self.assertEquals(block2.get_offset(), (-1, +1), "bad offset2")


    def DONTtest_add_to_space_blocks(self):
        verts1 = [(0, 0), (0, 12), (12, 12), (12, 0)]
        block1 = Block(verts1, (0, +12))
        verts2 = [(0, 0), (0, 12), (24, 12), (24, 0)]
        block2 = Block(verts2)
        body = RigidBody(block1, block2)

        body.add_to_space(Space(), (100, 200), 0)

        self.assertEquals(body.shapes, (block1, block2,), "shapes not added")

        poly1 = body.shapes[0].shape.get_points()
        expected = [
            Vec2d(92, 104), Vec2d(92, 116),
            Vec2d(104, 116), Vec2d(104, 104)]
        self.assertEquals(poly1, expected, "bad poly1 verts")

        poly2 = body.shapes[1].shape.get_points()
        expected = [
            Vec2d(92, 92), Vec2d(92, 104),
            Vec2d(116, 104), Vec2d(116, 92),
        ]
        self.assertEquals(poly2, expected, "bad poly2 verts")


    def test_space_add(self):
        from pymunk import Body, Poly, Space
        space = Space()
        body = Body(1, 1)
        body.position = (100, 200)

        verts1 = [(0, 0), (0, 20), (30, 20), (30, 0)]
        verts2 = [(0, 0), (0, 20), (30, 20), (30, 0)]
        poly1 = Poly(body, verts1, (10, 20))
        poly2 = Poly(body, verts2, (-30, -40))

        space.add(body)
        space.add(poly1)
        space.add(poly2)

        print poly1.get_points()
        print poly2.get_points()

        # 1
        self.assertEquals(body.position, Vec2d(100, 200), "body position")

        # 2
        expected = [(100, 200), (100, 220), (130, 220), (130, 200)]
        self.assertEquals(poly1.get_points(), expected, "bad verts")


        # 1
        self.assertEquals(body.position, Vec2d(100, 200), "body position")
        # 2
        expected = [(100, 200), (100, 220), (130, 220), (130, 200)]
        self.assertEquals(poly1.get_points(), expected, "bad verts")
        # 3
        expected = [(100, 200), (100, 220), (130, 220), (130, 200)]
        self.assertEquals(poly2.get_points(), expected, "bad verts")

        # 1
        self.assertEquals(body.position, Vec2d(100, 200), "body position")
        # 2
        expected = [(100, 200), (100, 220), (130, 220), (130, 200)]
        self.assertEquals(poly1.get_points(), expected, "bad verts")
        # 3
        expected = [(100, 200), (100, 220), (130, 220), (130, 200)]
        self.assertEquals(poly2.get_points(), expected, "bad verts")


    def test_add_to_space_discs(self):
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

