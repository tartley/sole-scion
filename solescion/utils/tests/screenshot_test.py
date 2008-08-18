from os import listdir, remove
from os.path import expanduser, join

from PIL import Image

from pyglet.window import Window
from pyglet import gl

import fixpath

from testutils.testcase import combine, MyTestCase, run_test

from utils.screenshot import _get_filename, image_from_window, save_screenshot


class Save_screenshot_test(MyTestCase):

    def test_get_filename(self):
        import utils.screenshot as screenshot_module
        orig = screenshot_module.listdir
        screenshot_module.listdir = lambda *_: ["A00.png"]
        try:
            self.assertEquals(
                _get_filename("A", ".png"),
                join(expanduser("~"), "A01.png"),
                "bad filename")
        finally:
            screenshot_module.listdir = orig


    def test_get_filename_none_left(self):
        import utils.screenshot as screenshot_module
        orig = screenshot_module.listdir
        screenshot_module.listdir = \
            lambda *_: ["A%02d.png" % idx for idx in range(100)]
        try:
            self.assertNone(_get_filename("A", ".png"), "expected None")
        finally:
            screenshot_module.listdir = orig


    def test_save_screenshot(self):
        window = Window(width=12, height=34, visible=False)

        import utils.screenshot as screenshot_module
        orig_get = screenshot_module._get_filename
        filename = join(expanduser("~"), "test_save_screenshot.png")
        screenshot_module._get_filename = lambda *_: filename
        try:
            try:
                save_screenshot(window)
            finally:
                screenshot_module._get_filename = orig_get

            image = Image.open(filename)
            self.assertEquals(image.size, (12, 34), "bad image")
        finally:
            remove(filename)


class Image_from_window_test(MyTestCase):

    def setUp(self):
        self.pixCols = {
            (0, 0): ( 0,    0,  40),
            (0, 1): ( 0,  200,  80),
            (1, 0): (100,   0, 120),
            (1, 1): (100, 200, 160),
            (2, 0): (200,   0, 200),
            (2, 1): (200, 200, 240),
        }

        self.window = Window(
            width=30, height=20, visible=False, caption="TestImage_from_window")
        self.window.on_resize(30, 20)
        self.window.dispatch_events()
        self.window.clear()

        gl.glBegin(gl.GL_POINTS)
        for loc, color in self.pixCols.iteritems():
            gl.glColor3ub(*color)
            gl.glVertex2f(*loc)
        gl.glEnd()


    def tearDown(self):
        self.window.close()


    def test_image_from_window(self):
        image = image_from_window(self.window)

        self.assertEquals(image.size, (self.window.width, self.window.height),
            "image size wrong")

        for (x, y), col in self.pixCols.iteritems():
            rgb = image.getpixel((x, self.window.height - 1 - y))[:3]
            self.assertEquals(rgb, col, "bad color at %d,%d" % (x, y))


    def test_image_from_window_returned_img_raises_on_bad_getpixel(self):
        image = image_from_window(self.window)

        invalidGet = lambda: image.getpixel((self.window.width+1, 0))
        self.assertRaises(invalidGet, IndexError)

        invalidGet = lambda: image.getpixel((0, self.window.height+1))
        self.assertRaises(invalidGet, IndexError)



Screenshot_test = combine(
    Image_from_window_test,
    Save_screenshot_test,
)

if __name__ == '__main__':
    run_test(Screenshot_test)
