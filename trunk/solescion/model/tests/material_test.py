#!/usr/bin/python -O

import fixpath

from solescion.testutils.testcase import MyTestCase, run

from solescion.model import material as module
from solescion.model.material import all_materials

class Material_test(MyTestCase):

    def test_materials(self):
        self.assertTrue(len(all_materials) > 4,  'not enough')

        for material in all_materials:
            self.assertTrue(material.density > 0,
                "bad density: %s" % (material.name,))
            self.assertTrue(0 <= material.elasticity <= 1,
                "bad elasticity: %s" % (material.name,))
            self.assertTrue(material.friction >= 0,
                "bad friction: %s" % (material.name,))
            self.assertValidColor(material.color,
                "bad color: %s" % (material.name,))
            self.assertEquals(getattr(module, material.name), material,
                "not on module: %s" % (material.name,))

if __name__ == "__main__":
    run(Material_test)
