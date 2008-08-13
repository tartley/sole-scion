#!/usr/bin/python -O

from pymunk import Body, moment_for_poly, Poly, Shape, Space, Vec2d

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from utils.geometry import poly_area
from model.shapes.block import Block


class Block_test(MyTestCase):

    def test_constructor(self):
        verts = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
        block = Block(verts, (5, 6))

        self.assertEquals(block.verts, verts, "didnt store verts")
        self.assertEquals(block.offset, (5.0, 6.0), "didnt store offset")
        self.assertEquals(block.mass, poly_area(verts), "mass wrong")
        self.assertNone(block.shape, "bad shape")
        self.assertValidColor(block.color)


    def test_constructor_defaults_offset_to_zero(self):
        verts = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
        block = Block(verts)
        self.assertEquals(block.offset, (0, 0), "bad default offset")
        self.assertEquals(block.verts, verts, "bad verts")


    def test_constructor_validates_verts(self):
        listener = Listener()
        verts = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
        from model.shapes import block as block_module
        orig = block_module.assert_valid_poly
        block_module.assert_valid_poly = listener
        try:
            block = Block(verts)
        finally:
            block_module.assert_valid_poly = orig
        self.assertEquals(listener.args, (verts,), "didnt validate verts")


    def test_constructor_centralizes_verts(self):
        verts = [(0, 0), (9, 12), (6, 0)]
        block = Block(verts)
        self.assertEquals(block.offset, (5, 4), "didnt update offset")
        expected = [(-5, -4), (4, 8), (1, -4)]
        self.assertEquals(block.verts, expected, "didnt update verts")


    def test_centralize_verts_should_leave_moment_unchanged(self):
        verts = [(0, 0), (0, 10), (20, 0)]
        block = Block(verts, (100, 200))
        m1 = moment_for_poly(block.mass, verts, (100, 200))
        self.assertEquals(m1, block.get_moment(), "moment changed")


    def test_get_moment(self):
        verts = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
        offset = (5, 6)
        block = Block(verts, offset)
        expected = moment_for_poly(block.mass, verts, offset)
        self.assertEquals(block.get_moment(), expected, "moment wrong")


    def test_add_to_body(self):
        space = Space()
        body = Body(10, 20)
        verts = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
        block = Block(verts, (1, 2))

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


