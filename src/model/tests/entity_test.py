#!/usr/bin/python -O

from __future__ import division
from math import pi

from pymunk import Body, Circle, moment_for_circle, Space, Vec2d

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.entity import Entity
from model.shapes.disc import Disc


class MockShape(object):
    def __init__(self, mass, offset=None, moment=None):
        self.mass = mass
        self.offset = offset
        self.get_moment = lambda: moment


class Entity_test(MyTestCase):

    def test_constructor(self):
        ent = Entity()
        self.assertEquals(type(ent.body), Body, "didnt create body")
        self.assertEquals(ent.body.mass, 0.0, "bad mass")
        self.assertEquals(ent.body.moment, 0.0, "bad moment")
        self.assertEquals(ent.body.position, Vec2d(0.0, 0.0), "bad position")
        self.assertEquals(ent.body.angle, 0.0, "bad angle")
        self.assertEquals(ent.shapes, [], "bad shapes")


    def test_constructor_takes_optional_shapes(self):
        ent = Entity()
        ent.add_shape = Listener()
        sh1 = Disc(1)
        sh2 = Disc(2)
        sh3 = Disc(3)
        ent.__init__(sh1, sh2, sh3)
        self.assertEquals(ent.add_shape.argsList, [(sh1,), (sh2,), (sh3,)],
            "shapes not addded")


    def test_position_read_from_body(self):
        ent = Entity()
        ent.body.position = (55, 66)
        ent.body.angle = 1.45
        self.assertEquals(ent.position, Vec2d(55, 66), "didnt use body position")
        self.assertAlmostEquals(ent.angle, 1.45, msg="didnt use body angle")


    def test_center_of_gravity(self):
        ent = Entity()

        obj1 = MockShape(2, offset=(10, 20))
        ent.shapes.append(obj1)
        ent.body.mass += obj1.mass
        self.assertEquals(ent._center_of_gravity(), (10, 20), "bad COG1")

        obj2 = MockShape(6, offset=(100, 50))
        ent.shapes.append(obj2)
        ent.body.mass += obj2.mass
        x = (600 + 20) / 8
        y = (300 + 40) / 8
        self.assertEquals(ent._center_of_gravity(), (x, y), "bad COG2")


    def test_offset_position(self):
        ent = Entity()
        ent.body.position = (100, 200)
        sh1 = MockShape(None, offset=(10, 20))
        sh2 = MockShape(None, offset=(30, 40))
        ent.shapes = [sh1, sh2]

        ent._offset_position((+2, -3))

        self.assertEquals(ent.body.position, Vec2d(102, 197),
            "bad body position")
        self.assertEquals(ent.shapes[0].offset, (8, 23), "bad sh1 offset")
        self.assertEquals(ent.shapes[1].offset, (28, 43), "bad sh2 offset")


    def test_get_moment(self):
        ent = Entity()
        sh1 = MockShape(None, moment=5)
        sh2 = MockShape(None, moment=10)
        ent.shapes = [sh1, sh2]

        self.assertEquals(ent.get_moment(), 15.0, "bad moment")


    def test_add_shape_disc(self):
        radius = 4
        offset = (3, 2)
        disc = Disc(radius, offset)

        ent = Entity()
        ent.add_shape(disc)

        expectedMass = pi * radius * radius
        self.assertAlmostEquals(ent.body.mass, expectedMass, places=5,
            msg="bad mass")
        expectedMoment = moment_for_circle(expectedMass, 0, radius, (0, 0))
        self.assertEquals(ent.body.moment, expectedMoment, "bad moment")
        self.assertEquals(ent.body.position, Vec2d(3, 2), "bad position")

        self.assertEquals(ent.shapes, [disc], "bad shapes")


    def test_add_to_space(self):
        disc1 = Disc(1)
        disc2 = Disc(2)
        disc3 = Disc(3)
        ent = Entity(disc1, disc2, disc3)
        space = Space()

        ent.add_to_space(space, (1, 2), 0.75)

        self.assertEquals(ent.body.position, Vec2d(1, 2), "bad position")
        self.assertEquals(ent.body.angle, 0.75, "bad angle")

        self.assertEquals(space.bodies, set([ent.body]),
            "body not added to space")

        radii = set()
        for circle in space.shapes:
            self.assertEquals(circle.body, ent.body, "bad Circle body")
            self.assertEquals(circle.friction, 0.5, "bad friction")
            self.assertEquals(circle.elasticity, 0.5, "bad elasticity")
            radii.add(circle.radius)
        self.assertEquals(radii, set([1, 2, 3]), "bad radii")


if __name__ == "__main__":
    run_test(Entity_test)

