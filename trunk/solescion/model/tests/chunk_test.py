#!/usr/bin/python -O

from __future__ import division
from math import pi

from pymunk import Body, Circle, moment_for_circle, Space, Vec2d

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.chunk import Chunk
from model.material import gold
from model.shards.block import Block
from model.shards.disc import Disc


class Chunk_test(MyTestCase):

    def setUp(self):
        self.unitsquare = [(0, 0), (0, 1), (1, 1), (1, 0)]


    def test_constructor(self):
        chunk = Chunk()
        self.assertNone(chunk.body, "bad body")
        self.assertEquals(chunk.shards, (), "bad shards")


    def test_constructor_adds_optional_shards(self):
        orig = Chunk.set_shards
        Chunk.set_shards = Listener()
        try:
            shard1 = Disc(gold, 1)
            shard2 = Disc(gold, 2)
            shard3 = Disc(gold, 3)
            chunk = Chunk(shard1, shard2, shard3)
            self.assertEquals(
                chunk.set_shards.argsList,
                [(shard1, shard2, shard3),],
                "shards not addded")
        finally:
            Chunk.set_shards = orig


    def test_position_read_from_body(self):
        chunk = Chunk()
        self.assertNone(chunk.position, "bad initial position")
        self.assertNone(chunk.angle, "bad initial angle")

        space = Space()

        chunk.add_to_space(space, (11, 22), 0.456)
        self.assertEquals(chunk.position, Vec2d(11, 22), "bad position")
        self.assertAlmostEquals(chunk.angle, 0.456, places=7,
            msg="bad angle")


    def test_center_of_gravity(self):
        chunk = Chunk()
        self.assertEquals(chunk._center_of_gravity(), (0, 0), "bad COG0")

        shard1 = Disc(gold, 2, (10, 20))
        chunk = Chunk()
        chunk.shards = (shard1,)
        cog = chunk._center_of_gravity()
        self.assertAlmostEquals(cog[0], 10, msg="bad COG1 x")
        self.assertAlmostEquals(cog[1], 20, msg="bad COG1 y")

        verts = [(99, 49), (99, 51), (101, 51), (101, 49)]
        shard2 = Block(gold, verts)
        chunk.shards = (shard2,)
        self.assertEquals(chunk._center_of_gravity(), (100, 50), "bad COG2")

        chunk.shards = (shard1, shard2)
        totalMass = shard1.mass + shard2.mass
        x = (10 * shard1.mass + 100 * shard2.mass) / totalMass
        y = (20 * shard1.mass + 50 * shard2.mass) / totalMass
        self.assertEquals(chunk._center_of_gravity(), (x, y), "bad COG3")


    def test_offset_shards(self):
        chunk = Chunk()
        shard1 = Disc(gold, 5, (10, 20))
        shard2 = Block(gold, self.unitsquare, (30, 40), center=True)
        chunk.shards = [shard1, shard2]

        chunk._offset_shards((+2, -3))

        offset1 = chunk.shards[0].get_offset()
        self.assertEquals(offset1, (12, 17), "bad shard1 offset")
        offset2 = chunk.shards[1].get_offset()
        self.assertEquals(offset2, (32, 37), "bad shard2 offset")


    def test_get_moment(self):
        chunk = Chunk()
        self.assertEquals(chunk.get_moment(), 0.0, "bad initial moment")

        shard1 = Disc(gold, 2, (10, 20))
        shard2 = Block(gold, self.unitsquare, (100, 200))
        chunk.shards = [shard1, shard2]

        expected = shard1.get_moment() + shard2.get_moment()
        self.assertEquals(chunk.get_moment(), expected, "bad moment")


    def test_get_mass(self):
        chunk = Chunk()
        self.assertEquals(chunk.get_mass(), 0.0, "bad initial mass")

        shard1 = Disc(gold, 5)
        shard2 = Block(gold, self.unitsquare)
        chunk.shards = [shard1, shard2]
        self.assertEquals(chunk.get_mass(), (25*pi+1)*gold.density, "bad mass")


    def test_set_shards_disc(self):
        radius = 4
        offset = (3, 2)
        disc = Disc(gold, radius, offset)
        chunk = Chunk()
        chunk.set_shards(disc)

        self.assertEquals(chunk.shards, (disc,), "bad shards")
        shard = chunk.shards[0]
        self.assertEquals(shard.get_offset(), (0, 0))


    def test_set_shards_two_discs(self):
        disc1 = Disc(gold, 4, (+100, +200))
        disc2 = Disc(gold, 2, (+115, +225))

        chunk = Chunk()
        chunk.set_shards(disc1, disc2)
        self.assertEquals(chunk.shards, (disc1, disc2), "bad shards")
        shard1offset = chunk.shards[0].get_offset()
        self.assertAlmostEquals(shard1offset[0], -3.0, msg="bad offset1 x")
        self.assertAlmostEquals(shard1offset[1], -5.0, msg="bad offset1 y")
        shard2offset = chunk.shards[1].get_offset()
        self.assertAlmostEquals(shard2offset[0], +12.0, msg="bad offset2 x")
        self.assertAlmostEquals(shard2offset[1], +20.0, msg="bad offset2 y")


    def test_set_shards_block(self):
        verts = [(0, 0), (0, 1), (1, 1), (1, 0)]
        offset = (10, 20)
        block = Block(gold, verts, offset)
        self.assertEquals(block.get_offset(), (10.5, 20.5), "bad offset")

        chunk = Chunk()
        chunk.set_shards(block)

        self.assertEquals(chunk.shards, (block,), "bad shards")
        shard = chunk.shards[0]
        self.assertEquals(shard.get_offset(), (0, 0), "bad offset")


    def test_set_shards_two_blocks(self):
        verts1 = [(0, 0), (0, 4), (4, 4), (4, 0)]
        block1 = Block(gold, verts1, (8, 0))
        verts2 = [(0, 0), (0, 4), (12, 4), (12, 0)]
        block2 = Block(gold, verts2, (0, 4))
        chunk = Chunk(block1, block2)

        self.assertEquals(chunk.shards, (block1, block2,), "shards not added")
        self.assertEquals(block1.get_offset(), (+3, -3), "bad offset1")
        self.assertEquals(block2.get_offset(), (-1, +1), "bad offset2")


    def DONTtest_add_to_space_blocks(self):
        verts1 = [(0, 0), (0, 12), (12, 12), (12, 0)]
        block1 = Block(gold, verts1, (0, +12))
        verts2 = [(0, 0), (0, 12), (24, 12), (24, 0)]
        block2 = Block(gold, verts2)
        chunk = Chunk(block1, block2)
        space = Space()

        chunk.add_to_space((100, 200), 0)

        self.assertEquals(chunk.shards, (block1, block2,), "shards not added")

        poly1 = chunk.shards[0].shard.get_points()
        expected = [
            Vec2d(92, 104), Vec2d(92, 116),
            Vec2d(104, 116), Vec2d(104, 104)]
        self.assertEquals(poly1, expected, "bad poly1 verts")

        poly2 = chunk.shards[1].shard.get_points()
        expected = [
            Vec2d(92, 92), Vec2d(92, 104),
            Vec2d(116, 104), Vec2d(116, 92),
        ]
        self.assertEquals(poly2, expected, "bad poly2 verts")


    def test_add_to_space_discs(self):
        disc1 = Disc(gold, 1)
        disc2 = Disc(gold, 2)
        disc3 = Disc(gold, 3)
        space = Space()
        chunk = Chunk(disc1, disc2, disc3)

        chunk.add_to_space(space, (1, 2), 0.75)

        self.assertEquals(type(chunk.body), Body, "didnt create body")
        self.assertEquals(chunk.body.position, Vec2d(1, 2), "bad position")
        self.assertEquals(chunk.body.angle, 0.75, "bad angle")

        self.assertEquals(space.bodies, set([chunk.body]),
            "body not added to space")

        self.assertEquals(len(space.shapes), 3, "shapes not added to space")
        radii = set()
        for circle in space.shapes:
            self.assertEquals(circle.body, chunk.body, "bad Circle body")
            self.assertEquals(circle.friction, 0.5, "bad friction")
            self.assertEquals(circle.elasticity, 0.5, "bad elasticity")
            radii.add(circle.radius)
        self.assertEquals(radii, set([1, 2, 3]), "bad radii")


if __name__ == "__main__":
    run_test(Chunk_test)

