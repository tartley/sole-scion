from __future__ import division
from math import cos, pi, sin, sqrt

import fixpath

from pymunk import Vec2d

from solescion.testutils.testcase import combine, MyTestCase, run

from solescion.geom.poly import (
    assert_valid, circle, regular, irregular, offset_verts, area,
    centroid, rotate90, circle_center
)


class Creation_test(MyTestCase):

    def test_circle(self):
        actual = circle(2.0, 10)
        self.assertEquals(len(actual), 10)
        for vert in actual:
            mag = sqrt(vert[0] ** 2 + vert[1] ** 2)
            self.assertEquals(mag, 2.0, epsilon=10 ** -7)


    def test_regular_invalid_num_vertices(self):
        v1 = 0, 1
        v2 = 0, 0
        self.assertRaises(lambda: regular(0, v1, v2), ValueError)
        self.assertRaises(lambda: regular(1, v1, v2), ValueError)
        self.assertRaises(lambda: regular(2, v1, v2), ValueError)


    def test_regular_tri(self):
        v1 = 1.0, 0.0
        v2 = 0.0, 0.0
        actual = regular(3, v1, v2)
        expected = [v1, v2, (0.5, sqrt(0.75)),]
        self.assertVertsEqual(actual, expected)


    def test_regular_square(self):
        v1 = 1.0, 0.0
        v2 = 0.0, 0.0
        actual = regular(4, v1, v2)
        expected = [v1, v2, (0.0, 1.0), (1.0, 1.0),]
        self.assertVertsEqual(actual, expected)



class Assert_valid_test(MyTestCase):

    def test_assert_valid_ok(self):
        verts3 = [(0, 0), (0, 1), (1, 0)]
        assert_valid(verts3)

        verts4 = [(0, 0), (0, 2), (2, 2), (2, 0)]
        assert_valid(verts4)


    def test_assert_valid_too_few(self):
        self.assertRaises(
            lambda: assert_valid([]),
            TypeError, "need 3 or more verts: []")

        verts1 = [(0, 0)]
        self.assertRaises(
            lambda: assert_valid(verts1),
            TypeError, 'need 3 or more verts: %s' % (verts1,))

        verts2 = [(0, 0), (0, 1)]
        self.assertRaises(
            lambda: assert_valid(verts2),
            TypeError, 'need 3 or more verts: %s' % (verts2,))


    def test_assert_valid_colinear_are_ok(self):
        colinear = [(0, 0), (1, 1), (2, 2)]
        self.assertRaises(
            lambda: assert_valid(colinear),
            TypeError, "colinear: %s" % (colinear,))


    def test_assert_valid_nonconvex(self):
        verts4n = [(3, 0), (0, 0), (0, 3), (1, 1)]
        self.assertRaises(
            lambda: assert_valid(verts4n),
            TypeError, 'not convex: %s' % (verts4n,))


    def test_assert_valid_counterclockwise(self):
        verts3cw = [(0, 1), (0, 0), (1, 0)]
        self.assertRaises(
            lambda: assert_valid(verts3cw),
            TypeError, 'anticlockwise winding: %s' % (verts3cw,))

        verts4cw = [(0, 2), (0, 0), (2, 0), (2, 2)]
        self.assertRaises(
            lambda: assert_valid(verts4cw),
            TypeError, 'anticlockwise winding: %s' % (verts4cw,))



class Offset_verts_test(MyTestCase):

    def test_offset_verts(self):
        verts = [(0, 1), (-2, -3), (4, 5)]
        self.assertEquals(
            offset_verts(verts, (10, 20)),
            [(10, 21), (8, 17), (14, 25)],
            "bad offset verts")


    def test_tuple_returns_tuple(self):
        verts = ((0, 1), (-2, -3), (4, 5))
        self.assertEquals(
            offset_verts(verts, (10, 20)),
            ((10, 21), (8, 17), (14, 25)),
            "bad offset tuple verts")


    def test_degenerate_cases(self):
        self.assertEquals(offset_verts([], (1, 1)), [], "bad for empty list")
        self.assertEquals(offset_verts((), (1, 1)), (), "bad for empty tuple")



class Area_test(MyTestCase):

    def test_area_unit_square(self):
        verts = [(0, 0), (0, 1), (1, 1), (1, 0)]
        self.assertEquals(area(verts), 1.0, "bad unit square area")
        verts.reverse()
        self.assertEquals(area(verts), -1.0,
            "bad clockwise unit square area")


    def test_area_circle(self):
        verts = []
        numSegments = 1000
        for idx in range(numSegments):
            theta = 2 * pi * idx / numSegments
            verts.append((sin(theta), cos(theta)))
        self.assertAlmostEquals(area(verts), pi, places=4,
            msg="bad circle area")
        verts.reverse()
        self.assertAlmostEquals(area(verts), -pi, places=4,
            msg="bad clockwise circle area")



class Centroid_test(MyTestCase):

    def test_centroid_unit_square(self):
        verts = [(0,0), (0,1), (1,1), (1,0)]
        self.assertEquals(centroid(verts), (0.5, 0.5),
            "bad centroid unitsquare")


    def test_centroid_big_slanty_square(self):
        verts = [(90,100), (100,110), (110,100), (100,90)]
        self.assertEquals(centroid(verts), (100, 100),
            "bad centroid big slanty square")


    def test_centroid_triangle(self):
        verts = [(2, 2), (4, 2), (6, 5)]
        self.assertEquals(centroid(verts), (4, 3),
            "bad centroid big slanty square")


    def test_centroid_triangle_counterclockwise(self):
        verts = [(2, 2), (4, 2), (6, 5)]
        verts.reverse()
        self.assertEquals(centroid(verts), (4, 3),
            "bad centroid big slanty square")


    def test_centroid_regular_octagon(self):
        verts = [
            (80, 90),
            (80, 110),
            (90, 120),
            (110, 120),
            (120, 110),
            (120, 90),
            (110, 80),
            (90, 80),
        ]
        self.assertEquals(centroid(verts), (100, 100),
            "bad centroid big slanty square")


    def test_centroid_clustered_verts(self):
        verts = [
            (1, 0),
            (0.3, 0),
            (0.2, 0),
            (0.1, 0),
            (0, 0),
            (0, 0.1),
            (0, 0.2),
            (0, 0.3),
            (0, 1),
            (1, 1),
        ]
        self.assertEquals(centroid(verts), (0.5, 0.5),
            "bad centroid unitsquare")



class Circle_center_test(MyTestCase):

    def test_rotate90(self):
        self.assertEquals(rotate90(Vec2d(1, 2)), Vec2d(-2, 1))


    def test_circle_center(self):
        start = Vec2d(97, 10)
        face = Vec2d(6, 0)
        radius = 5
        center = circle_center(start, face, radius)
        self.assertEquals(center, Vec2d(100, 6))


    def test_circle_center_impossible(self):
        start = Vec2d(-10, 0)
        face = Vec2d(20, 0)
        radius = 9
        self.assertRaises(
            lambda: circle_center(start, face, radius), ValueError)



class Irregular_test(MyTestCase):

    def test_irregular(self):
        start = Vec2d(3, -4)
        face = Vec2d(-6, 0)
        radius = 5
        # irregular poly's circle center is at (0, 0)
        num_verts = 5
        actual = irregular(start, face, radius, num_verts)
        print actual
        self.assertEquals(len(actual), 5)
        self.assertEquals(actual[0], Vec2d(+3, -4))
        self.assertEquals(actual[1], Vec2d(-3, -4))
        for point in actual:
            self.assertAlmostEquals(point.get_length_sqrd(), 25.0)


    def test_irregular_impossible(self):
        start = Vec2d(-10, -0)
        face = Vec2d(20, 0)
        radius = 9
        num_verts = 3
        self.assertRaises(
            lambda: irregular(start, face, radius, num_verts), ValueError)



Poly_test = combine(
    Creation_test,
    Assert_valid_test,
    Offset_verts_test,
    Area_test,
    Centroid_test,
    Circle_center_test,
    Irregular_test,
)

if __name__ == "__main__":
    run(Poly_test)

