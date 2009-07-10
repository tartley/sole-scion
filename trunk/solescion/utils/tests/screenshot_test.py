from os import listdir, remove
from os.path import expanduser, join

from pyglet import gl
from pyglet import image
from pyglet.window import Window

import fixpath

from solescion.testutils.testcase import MyTestCase, run

from solescion.utils.screenshot import _get_filename, save_screenshot


class Screenshot_test(MyTestCase):

    def setUp(self):
        self.window = None

    def tearDown(self):
        if self.window:
            self.window.close()


    def test_get_filename(self):
        import solescion.utils.screenshot as screenshot_module
        orig = screenshot_module.listdir
        screenshot_module.listdir = lambda *_: ["A000.png"]
        try:
            self.assertEquals(
                _get_filename("A", ".png"),
                join(expanduser("~"), "A001.png"),
                "bad filename")
        finally:
            screenshot_module.listdir = orig


    def test_get_filename_none_left(self):
        import solescion.utils.screenshot as screenshot_module
        orig = screenshot_module.listdir
        screenshot_module.listdir = \
            lambda *_: ["A%03d.png" % idx for idx in range(101)]
        try:
            self.assertNone(_get_filename("A", ".png"), "expected None")
        finally:
            screenshot_module.listdir = orig


    def test_save_screenshot(self):
        self.window = Window(
            width=12, height=34, visible=False,
            caption='test_save_screenshot',
        )
        import solescion.utils.screenshot as screenshot_module
        orig_get = screenshot_module._get_filename
        filename = join(expanduser("~"), "test_save_screenshot.png")
        screenshot_module._get_filename = lambda *_: filename
        try:
            try:
                save_screenshot(self.window)
            finally:
                screenshot_module._get_filename = orig_get

            png = image.load(filename)
            self.assertEquals((png.width, png.height), (12, 34), "bad image")
        finally:
            remove(filename)


if __name__ == '__main__':
    run(Save_screenshot_test)
