#!/usr/bin/python -O

from pymunk import Body, moment_for_poly, Poly, Shape, Space, Vec2d
from shapely.geometry import Polygon

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.shapes.block import Block


class Block_test(MyTestCase):

    def test_constructor(self):
        verts = [(0, 1), (-1, 4), (2, 3)]
        block = Block(5, 6, verts)

        self.assertEquals(block.offset, (5.0, 6.0), "didnt store offset")
        self.assertEquals(block.verts, verts, "didnt store verts")
        poly = Polygon(verts)
        self.assertEquals(block.mass, Polygon(verts).area, "mass wrong")
        expected = moment_for_poly(block.mass, verts, (5, 6))
        self.assertEquals(block.moment, expected, "moment wrong")


    def test_constructor_validates_verts(self):
        listener = Listener()
        verts = [(0, 1), (2, 3), (-1, 4)]
        from model.shapes import block as block_module
        orig = block_module.assert_valid_poly
        block_module.assert_valid_poly = listener
        try:
            block = Block(5, 6, verts)
        finally:
            block_module.assert_valid_poly = orig
        self.assertEquals(listener.args, (verts,), "didnt validate verts")


    def test_add_to_body(self):
        space = Space()
        body = Body(10, 20)
        verts = [(0, 1), (-1, 4), (2, 3)]
        block = Block(1, 2, verts)

        block.add_to_body(space, body)

        self.assertEquals(type(block.shape), Poly, "didnt create shape")
        self.assertEquals(block.shape.body, body, "didnt add shape to body")
        shapeVerts = block.shape.get_points()
        expected = [Vec2d(v) for v in verts]
        self.assertEquals(shapeVerts, expected, "bad shape verts")
        self.assertEquals(block.shape.friction, 0.5, "bad shape friction")
        self.assertEquals(block.shape.elasticity, 0.5, "bad shape elasticity")
        spaceShape = space.shapes.pop()
        self.assertEquals(block.shape, spaceShape, "didn't add shape to space")


if __name__ == "__main__":
    run_test(Block_test)


