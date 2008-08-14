#!/usr/bin/python -O

from pymunk import Body, moment_for_poly, Poly, Shape, Space, Vec2d

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from utils.geometry import offset_verts, poly_area
from model.shards.block import Block


class Block_test(MyTestCase):

    def test_constructor(self):
        verts = [(-1, -2), (-3, +4), (+5, +6), (+7, -8)]
        block = Block(verts)
        self.assertEquals(block.verts, verts, "bad verts")

        self.assertEquals(block.mass, poly_area(verts), "mass wrong")
        self.assertNone(block.shape, "bad shape")
        self.assertValidColor(block.color)


    def test_constructor_validates_verts(self):
        listener = Listener()
        verts = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
        from model.shards import block as block_module
        orig = block_module.assert_valid_poly
        block_module.assert_valid_poly = listener
        try:
            block = Block(verts)
        finally:
            block_module.assert_valid_poly = orig
        self.assertEquals(listener.args, (verts,), "didnt validate verts")


    def test_constructor_applies_offset(self):
        verts = [(-1, -2), (-3, +4), (+5, +6), (+7, -8)]
        offset = (5, 6)
        block = Block(verts, offset)

        expected = offset_verts(verts, offset)
        self.assertEquals(block.verts, expected, "didnt apply offset")


    def test_constructor_centers(self):
        verts = [(0, 0), (9, 12), (6, 0)]
        block = Block(verts, center=True)
        expected = [(-5, -4), (4, 8), (1, -4)]
        self.assertEquals(block.verts, expected, "didnt centralize verts")


    def test_constructor_centres_then_offsets(self):
        verts = [(0, 0), (9, 12), (6, 0)]
        block = Block(verts, center=True, offset=(10, 20))
        expected = [(5, 16), (14, 28), (11, 16)]
        self.assertEquals(block.verts, expected,
            "didnt apply center and offset right")


    def test_get_moment(self):
        verts = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
        offset = (5, 6)
        block = Block(verts, offset)
        expected = moment_for_poly(block.mass, verts, offset)
        self.assertEquals(block.get_moment(), expected, "moment wrong")


    def test_get_offset(self):
        verts = [(10, 20), (10, 24), (12, 24), (12, 20)]
        block = Block(verts, (100, 200))
        self.assertEquals(block.get_offset(), (111, 222), "bad offset")


    def test_offset(self):
        verts = [(-1, -2), (-3, +4), (+5, +6), (+7, -8)]
        block = Block(verts, (10, 20))
        block.offset((100, 200))
        expected = [(109, 218), (107, 224), (115, 226), (117, 212)]
        self.assertEquals(block.verts, expected, "didnt apply offset")


    def test_add_to_body(self):
        space = Space()
        body = Body(10, 20)
        verts = [(-1, -1), (-1, +1), (+1, +1), (+1, -1)]
        offset = (1, 2)
        block = Block(verts, offset)

        block.add_to_body(space, body)

        self.assertEquals(type(block.shape), Poly, "didnt create shape")
        self.assertEquals(block.shape.body, body, "didnt add shape to body")
        shapeVerts = block.shape.get_points()
        expected = [Vec2d(v) for v in offset_verts(verts, offset)]
        self.assertEquals(shapeVerts, expected, "bad shape verts")
        self.assertEquals(block.shape.friction, 0.5, "bad shape friction")
        self.assertEquals(block.shape.elasticity, 0.5, "bad shape elasticity")
        spaceShape = [s for s in space.shapes][0]
        self.assertEquals(block.shape, spaceShape, "didn't add shape to space")


if __name__ == "__main__":
    run_test(Block_test)


