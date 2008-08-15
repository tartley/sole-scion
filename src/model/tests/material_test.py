#!/usr/bin/python -O

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.material import Materials


class Material_test(MyTestCase):

    def test_materials(self):
        mats = set()
        for name, mat in Materials.__dict__.iteritems():
            if name.startswith('__'):
                continue
            mats.add(mat)
            self.assertTrue(mat.density > 0, "bad density: %s" % (name,))
            self.assertTrue(0 <= mat.elasticity <= 1,
                "bad elasticity: %s" % (name,))
            self.assertTrue(mat.friction >= 0, "bad friction: %s" % (name,))
            self.assertValidColor(mat.color, "bad color: %s" % (name,))

        self.assertTrue(len(mats) > 4, "not enough materials")


if __name__ == "__main__":
    run_test(Material_test)
