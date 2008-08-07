#!/usr/bin/python -O

from __future__ import division
from math import cos, sin, pi

from shapely.geometry import Polygon

import fixpath

from testutils.testcase import MyTestCase, run_test

from utils.geometry import assert_valid_poly, poly_area


class Geometry_test(MyTestCase):

    def test_assert_valid_poly_ok(self):
        verts3y = [(0, 0), (0, 1), (1, 0)]
        assert_valid_poly(verts3y)

        verts4y = [(0, 0), (0, 2), (2, 2), (2, 0)]
        assert_valid_poly(verts4y)


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


    def test_assert_valid_poly_bad(self):
        verts3c = [(0, 0), (1, 1), (2, 2)]
        self.assertRaises(
            lambda: assert_valid_poly(verts3c),
            TypeError, 'verts are colinear: %s' % (verts3c,))

        verts4n = [(3, 0), (0, 0), (0, 3), (1, 1)]
        self.assertRaises(
            lambda: assert_valid_poly(verts4n),
            TypeError, 'not convex: %s' % (verts4n,))


    def test_assert_valid_poly_counterclockwise(self):
        verts3cw = [(0, 1), (0, 0), (1, 0)]
        self.assertRaises(
            lambda: assert_valid_poly(verts3cw),
            TypeError, 'clockwise winding: %s' % (verts3cw,))

        verts4cw = [(0, 2), (0, 0), (2, 0), (2, 2)]
        self.assertRaises(
            lambda: assert_valid_poly(verts4cw),
            TypeError, 'clockwise winding: %s' % (verts4cw,))


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


if __name__ == "__main__":
    run_test(Geometry_test)

