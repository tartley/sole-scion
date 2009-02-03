from __future__ import division
from math import cos, pi, sin, sqrt

import fixpath

from solescion.testutils.testcase import combine, MyTestCase, run

from solescion.geom.poly import (
    assert_valid_poly, create_regular, offset_verts, poly_area, poly_centroid
)


class Poly_test(MyTestCase):

    def test_create_regular_invalid_num_vertices(self):
        v1 = 0, 1
        v2 = 0, 0
        self.assertRaises(lambda: create_regular(0, v1, v2), ValueError)
        self.assertRaises(lambda: create_regular(1, v1, v2), ValueError)
        self.assertRaises(lambda: create_regular(2, v1, v2), ValueError)


    def test_create_regular_tri(self):
        v1 = 1.0, 0.0
        v2 = 0.0, 0.0
        actual = create_regular(3, v1, v2)
        expected = [v1, v2, (0.5, sqrt(0.75)),]
        self.assertVertsEqual(actual, expected)


    def test_create_regular_square(self):
        v1 = 1.0, 0.0
        v2 = 0.0, 0.0
        actual = create_regular(4, v1, v2)
        expected = [v1, v2, (0.0, 1.0), (1.0, 1.0),]
        self.assertVertsEqual(actual, expected)


class Assert_valid_poly_test(MyTestCase):

    def test_assert_valid_poly_ok(self):
        verts3 = [(0, 0), (0, 1), (1, 0)]
        assert_valid_poly(verts3)

        verts4 = [(0, 0), (0, 2), (2, 2), (2, 0)]
        assert_valid_poly(verts4)


    def test_assert_valid_poly_too_few(self):
        self.assertRaises(
            lambda: assert_valid_poly([]),
            TypeError, "need 3 or more verts: []")

        verts1 = [(0, 0)]
        self.assertRaises(
            lambda: assert_valid_poly(verts1),
            TypeError, 'need 3 or more verts: %s' % (verts1,))

        verts2 = [(0, 0), (0, 1)]
        self.assertRaises(
            lambda: assert_valid_poly(verts2),
            TypeError, 'need 3 or more verts: %s' % (verts2,))


    def test_assert_valid_poly_colinear_are_ok(self):
        colinear = [(0, 0), (1, 1), (2, 2)]
        self.assertRaises(
            lambda: assert_valid_poly(colinear),
            TypeError, "colinear: %s" % (colinear,))


    def test_assert_valid_poly_nonconvex(self):
        verts4n = [(3, 0), (0, 0), (0, 3), (1, 1)]
        self.assertRaises(
            lambda: assert_valid_poly(verts4n),
            TypeError, 'not convex: %s' % (verts4n,))


    def test_assert_valid_poly_counterclockwise(self):
        verts3cw = [(0, 1), (0, 0), (1, 0)]
        self.assertRaises(
            lambda: assert_valid_poly(verts3cw),
            TypeError, 'anticlockwise winding: %s' % (verts3cw,))

        verts4cw = [(0, 2), (0, 0), (2, 0), (2, 2)]
        self.assertRaises(
            lambda: assert_valid_poly(verts4cw),
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



class Poly_area_test(MyTestCase):

    def test_poly_area_unit_square(self):
        verts = [(0, 0), (0, 1), (1, 1), (1, 0)]
        self.assertEquals(poly_area(verts), 1.0, "bad unit square area")
        verts.reverse()
        self.assertEquals(poly_area(verts), -1.0,
            "bad clockwise unit square area")


    def test_poly_area_circle(self):
        verts = []
        numSegments = 1000
        for idx in range(numSegments):
            theta = 2 * pi * idx / numSegments
            verts.append((sin(theta), cos(theta)))
        self.assertAlmostEquals(poly_area(verts), pi, places=4,
            msg="bad circle area")
        verts.reverse()
        self.assertAlmostEquals(poly_area(verts), -pi, places=4,
            msg="bad clockwise circle area")


class Poly_centroid_test(MyTestCase):

    def test_poly_centroid_unit_square(self):
        verts = [(0,0), (0,1), (1,1), (1,0)]
        self.assertEquals(poly_centroid(verts), (0.5, 0.5),
            "bad centroid unitsquare")


    def test_poly_centroid_big_slanty_square(self):
        verts = [(90,100), (100,110), (110,100), (100,90)]
        self.assertEquals(poly_centroid(verts), (100, 100),
            "bad centroid big slanty square")


    def test_poly_centroid_triangle(self):
        verts = [(2, 2), (4, 2), (6, 5)]
        self.assertEquals(poly_centroid(verts), (4, 3),
            "bad centroid big slanty square")


    def test_poly_centroid_triangle_counterclockwise(self):
        verts = [(2, 2), (4, 2), (6, 5)]
        verts.reverse()
        self.assertEquals(poly_centroid(verts), (4, 3),
            "bad centroid big slanty square")


    def test_poly_centroid_regular_octagon(self):
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
        self.assertEquals(poly_centroid(verts), (100, 100),
            "bad centroid big slanty square")


    def test_poly_centroid_clustered_verts(self):
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
        self.assertEquals(poly_centroid(verts), (0.5, 0.5),
            "bad centroid unitsquare")


Geometry_test = combine(
    Poly_test,
    Assert_valid_poly_test,
    Offset_verts_test,
    Poly_area_test,
    Poly_centroid_test,
)

if __name__ == "__main__":
    run(Geometry_test)

