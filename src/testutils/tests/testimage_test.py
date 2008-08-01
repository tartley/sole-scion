#!/usr/bin/python -O
from __future__ import division

from PIL import Image
from pyglet import gl
from pyglet.window import Window

import fixpath

from testutils.testcase import combine, MyTestCase, run_test

from testutils.testimage import (
    assert_contains, assert_entirely,
    assert_rectangle_at, image_from_window, save_to_tempfile
)


window = Window(width=3, height=2)


def draw_rectangle(image, left, bottom, right, top, rectCol):
    for x in range(left, right+1):
        for y in range(bottom, top+1):
            image.putpixel((x,y), rectCol)


class TestImage_from_window_test(MyTestCase):

    def setUp(self):
        global window
        self.pixCols = {
            (0, 0): ( 0,    0,  40),
            (0, 1): ( 0,  200,  80),
            (1, 0): (100,   0, 120),
            (1, 1): (100, 200, 160),
            (2, 0): (200,   0, 200),
            (2, 1): (200, 200, 240),
        }

        window.dispatch_events()

        gl.glBegin(gl.GL_POINTS)
        for loc, color in self.pixCols.iteritems():
            gl.glColor3ub(*color)
            gl.glVertex2f(*loc)
        gl.glEnd()


    def test_image_from_window(self):
        global window
        image = image_from_window(window)

        self.assertEquals(image.size, (window.width, window.height),
            "image size wrong")

        for x in range(window.width):
            for y in range(window.height):
                rgb = image.getpixel((x, window.height - 1 - y))[:3]
                self.assertEquals(rgb, self.pixCols[(x, y)],
                    "bad color at %d,%d" % (x, y))


    def test_image_from_window_returned_img_raises_on_bad_getpixel(self):
        global window
        image = image_from_window(window)

        invalidGet = lambda: image.getpixel((window.width+1, 0))
        self.assertRaises(invalidGet, IndexError)

        invalidGet = lambda: image.getpixel((0, window.height+1))
        self.assertRaises(invalidGet, IndexError)


class TestImage_assert_test(MyTestCase):

    def test_assert_entirely(self):
        backCol = (111, 22, 3)
        image = Image.new('RGB', (20, 10), backCol)
        assert_entirely(image, backCol)
        assert_entirely(image, backCol, "dontmatter")

        newCol = (111, 22, 4)
        image.putpixel((10, 5), newCol)

        assertion = lambda: assert_entirely(image, backCol)
        expectedMsg = '%s != %s\n  pixel %d,%d wrong color\n  ' % \
            (newCol, backCol, 10, 5)
        self.assertRaises(assertion, AssertionError, expectedMsg)

        assertion = lambda: assert_entirely(image, backCol, 'desc')
        expectedMsg = '%s != %s\n  pixel %d,%d wrong color\n  desc' % \
            (newCol, backCol, 10, 5)
        self.assertRaises(assertion, AssertionError, expectedMsg)


    def test_assert_entirely_with_rgba(self):
        backCol = (111, 22, 3)
        image = Image.new('RGBA', (20, 10), backCol)
        assert_entirely(image, backCol)


    def test_assert_contains(self):
        backCol = (111, 22, 3)
        image = Image.new('RGB', (20, 10), backCol)

        newCol = (111, 22, 4)
        assertion = lambda: assert_contains(image, newCol)
        expectedMsg = 'does not contain %s. does contain:\n' \
            '  %s\n' % (newCol, set([backCol]))
        self.assertRaises(assertion, AssertionError, expectedMsg)

        assertion = lambda: assert_contains(image, newCol, 'desc')
        expectedMsg = 'does not contain %s. does contain:\n' \
            '  %s\ndesc' \
            % (newCol, set([backCol]))
        self.assertRaises(assertion, AssertionError, expectedMsg)

        image.putpixel((10, 5), newCol)
        assert_contains(image, newCol)


    def test_assert_contains_with_rgba(self):
        backCol = (111, 22, 3)
        image = Image.new('RGBA', (20, 10), backCol)
        assert_contains(image, backCol)


    def test_assert_rectangle_at_fails_if_degenerate(self):
        rectCol = (255, 255, 0)
        backCol = (0, 0, 255)
        image = Image.new('RGB', (20, 10), backCol)

        window_ords = [
            (1, 1, 1, 8),
            (1, 1, 2, 8),
            (1, 1, 8, 1),
            (1, 1, 8, 2),
        ]
        for ords in window_ords:
            assertion = lambda: assert_rectangle_at(
                image, ords[0], ords[1], ords[2], ords[3], rectCol, backCol)
            expectedMsg = "degenerate rect %d,%d %d,%d. Broken test?" % ords
            self.assertRaises(assertion, AssertionError, expectedMsg)


    def test_assert_rectangle_at_fails_if_touch_edge(self):
        backCol = (0, 0, 255)
        rectCol = (255, 255, 0)
        image = Image.new('RGB', (20, 10), backCol)

        window_ords = [
            (0, 1, 18, 8),
            (-1, 1, 18, 8),
            (1, 0, 18, 8),
            (1, -1, 18, 8),
            (1, 1, 19, 8),
            (1, 1, 20, 8),
            (1, 1, 18, 9),
            (1, 1, 18, 10),
        ]
        for ords in window_ords:
            assertion = lambda: assert_rectangle_at(
                image, ords[0], ords[1], ords[2], ords[3], rectCol, backCol)
            expectedMsg = "rect %d,%d %d,%d touches edge of (20, 10). " \
                "Broken test?" % ords
            self.assertRaises(assertion, AssertionError, expectedMsg)


    def test_assert_rectangle_at_fails_if_colors_same(self):
        color = (123, 45, 6)
        image = Image.new('RGB', (20, 10), color)
        assertion = lambda: assert_rectangle_at(
            image, 1, 1, 18, 8, color, color)
        expectedMsg = "colors are same %s. Broken test?" % (color,)
        self.assertRaises(assertion, AssertionError, expectedMsg)


    def test_assert_rectangle_at_passes(self):
        backCol = (123, 45, 6)
        image = Image.new('RGB', (20, 10), backCol)
        rectCol = (234, 56, 7)
        draw_rectangle(image, 2, 2, 17, 7, rectCol)
        assert_rectangle_at(image, 2, 2, 17, 7, rectCol, backCol)

        # and again, with rogue pixels just off each corner
        image.putpixel((1, 1), rectCol)
        image.putpixel((18, 1), rectCol)
        image.putpixel((1, 8), rectCol)
        image.putpixel((18, 8), rectCol)
        assert_rectangle_at(image, 2, 2, 17, 7, rectCol, backCol)


    def test_assert_rectangle_at_fails(self):
        backCol = (123, 45, 6)
        rectCol = (234, 56, 7)

        # if any one of these pixels are set, the assert should raise
        roguePixels = [
            (2, 2, backCol),
            (2, 4, backCol),
            (2, 7, backCol),
            (9, 2, backCol),
            (9, 7, backCol),
            (17, 2, backCol),
            (17, 4, backCol),
            (17, 7, backCol),
            (2, 1, rectCol),
            (9, 1, rectCol),
            (17, 1, rectCol),
            (2, 8, rectCol),
            (9, 8, rectCol),
            (17, 8, rectCol),
            (1, 2, rectCol),
            (1, 4, rectCol),
            (1, 7, rectCol),
            (18, 2, rectCol),
            (18, 4, rectCol),
            (18, 7, rectCol),
        ]
        for x, y, col in roguePixels:
            image = Image.new('RGB', (20, 10), backCol)
            draw_rectangle(image, 2, 2, 17, 7, rectCol)
            image.putpixel((x, y), col)

            assertion = lambda: assert_rectangle_at( \
                image, 2, 2, 17, 7, rectCol, backCol)
            expectedMsg = "rectangle 2,2 17,7 bad, eg at %d,%d" % (x, y)
            e = self.assertRaises(assertion, AssertionError)
            self.assertTrue(e.message.startswith(expectedMsg), \
                'assert_rectange_at raised with bad message')


    def test_assert_rectangle_at_with_rgba(self):
        backCol = (123, 45, 6)
        rectCol = (234, 56, 7)
        image = Image.new('RGBA', (20, 10), backCol)
        draw_rectangle(image, 2, 2, 17, 7, rectCol)
        assert_rectangle_at(image, 2, 2, 17, 7, rectCol, backCol)


TestImage_test = combine(
    TestImage_from_window_test,
    TestImage_assert_test,
)

if __name__ == "__main__":
    run_test()

