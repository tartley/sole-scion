#!/usr/bin/python -O

import fixpath

from solescion.testutils.testcase import MyTestCase, run_test

from solescion.model import material

class Material_test(MyTestCase):

    def test_materials(self):
        mats = set()
        for name, mat in material.__dict__.iteritems():
            if name.startswith('__') or name=='Material':
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
