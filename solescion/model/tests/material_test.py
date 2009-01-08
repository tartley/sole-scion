#!/usr/bin/python -O

import fixpath

from solescion.testutils.testcase import MyTestCase, run

from solescion.model.material import Material

class Material_test(MyTestCase):

    def test_materials(self):
        materials = set()
        for name in dir(Material):
            if name.startswith('_'):
                continue
            material = getattr(Material, name)
            materials.add(material)
            self.assertTrue(material.density > 0,
                "bad density: %s" % (name,))
            self.assertTrue(0 <= material.elasticity <= 1,
                "bad elasticity: %s" % (name,))
            self.assertTrue(material.friction >= 0,
                "bad friction: %s" % (name,))
            self.assertValidColor(material.color,
                "bad color: %s" % (name,))

        self.assertTrue(len(materials) > 4, "not enough materials")


if __name__ == "__main__":
    run(Material_test)
