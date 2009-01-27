from math import sqrt

import fixpath

from solescion.testutils.testcase import MyTestCase, run

from solescion.geom.poly import create_regular


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


if __name__ == '__main__':
    run(Poly_test)

