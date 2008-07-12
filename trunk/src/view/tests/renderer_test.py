from pyglet.window import Window
from pyglet.gl import (
    glClear, glClearColor, glGetFloatv, glReadBuffer, glReadPixels,
    GLfloat, GLubyte,
    GL_BACK, GL_COLOR_BUFFER_BIT, GL_COLOR_CLEAR_VALUE, GL_RGB,
    GL_UNSIGNED_BYTE,
)

import fix_pythonpath

from testutils.testcase import MyTestCase, run_test

from model.world import World
from view.renderer import Renderer


def getRgbArray(win, buff):
    numBytes = win.width * win.height * 3
    rgbs = (GLubyte * numBytes)(*(0 for _ in range(numBytes)))
    glReadBuffer(buff)
    glReadPixels(0, 0, win.width, win.height, GL_RGB, GL_UNSIGNED_BYTE, rgbs)
    return rgbs


def floats_to_ubytes(sequence):
    ubytes = (int(255 * x) for x in sequence)
    retType = type(sequence)
    return retType(ubytes)


class Renderer_test(MyTestCase):

    def testConstructor(self):
        window = object()
        world = object()
        renderer = Renderer(world, window)
        self.assertTrue(renderer.world is world, "should store model")
        self.assertTrue(renderer.window is window, "should store window")
        self.assertEquals(renderer.clearColor, (0.0, 0.0, 1.0, 1.0),
            "clearColor should default to blue")


    def assertRgbArrayIsEntirely(self, rgbs, expectedRgb, message=None):
        if message is None:
            message = ""
        for idx in range(0, len(rgbs), 3):
            r, g, b = rgbs[idx], rgbs[idx+1], rgbs[idx+2]
            self.assertEquals((r, g, b), expectedRgb,
                "pixel %d wrong color\n%s" % (idx, message))


    def assertRgbArrayContains(self, rgbs, expectedRgb, message=None):
        if message is None:
            message = ""
        found = set()
        for idx in range(0, len(rgbs), 3):
            r, g, b = rgbs[idx], rgbs[idx+1], rgbs[idx+2]
            if (r, g, b) == expectedRgb:
                return
            found.add((r, g, b))
            msg = "did not contain %s\ndid contain: %s\n%s" % \
                (expectedRgb, found, message)
            self.fail(msg)


    def testDraw_should_clear_hidden_buffer(self):
        width, height = 20, 10
        win = Window(width=width, height=height)
        try:
            renderer = Renderer(World(), win)

            # sanity check: after glClear, the surface should be clearColor
            win.dispatch_events()
            glClearColor(0.5, 0.5, 0.5, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            rgbs = getRgbArray(win, GL_BACK)
            self.assertRgbArrayIsEntirely(rgbs, (127, 127, 127), "sanity check")

            renderer.clearColor = (0.9, 0.8, 0.7, 1.0)
            renderer.draw()

            rgbs = getRgbArray(win, GL_BACK)
            expectedRgb = floats_to_ubytes(renderer.clearColor[:3])
            self.assertRgbArrayIsEntirely(rgbs, expectedRgb,
                "draw should clear to clearColor")
        finally:
            win.close()


    def testDraw_should_render_the_room(self):
        width, height = 400, 300
        world = World()
        world.populate()
        win = Window(width=width, height=height)
        try:
            renderer = Renderer(World(), win)
            win.dispatch_events()

            renderer.draw()

            rgbs = getRgbArray(win, GL_BACK)
            expectedRgb = floats_to_ubytes(renderer.clearColor[:3])
            self.assertRgbArrayContains(rgbs, expectedRgb,
                "should contains some clearColor")

            room = [room for room in world.rooms][0]
            expectedRgb = floats_to_ubytes(room.color)
            self.assertRgbArrayContains(rgbs, expectedRgb,
                "should draw some room color")
        finally:
            win.close()


if __name__ == "__main__":
    run_test()

