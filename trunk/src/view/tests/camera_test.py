#!/usr/bin/python -O

from pyglet.window import Window
from pyglet.gl import (
    glClear, glClearColor, glGetFloatv, glReadBuffer, glReadPixels,
    GLfloat, GLubyte,
    GL_BACK, GL_COLOR_BUFFER_BIT, GL_COLOR_CLEAR_VALUE, GL_RGB,
    GL_UNSIGNED_BYTE,
)

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.world import Room, World
from view.camera import Camera


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


class Camera_test(MyTestCase):

    def testConstructor(self):
        window = object()
        world = object()
        camera = Camera(world, window)
        self.assertTrue(camera.world is world, "should store model")
        self.assertTrue(camera.window is window, "should store window")


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
            found.add((r, g, b))
            if (r, g, b) == expectedRgb:
                return
        msg = "did not contain %s\ndid contain: %s\n%s" % \
            (expectedRgb, found, message)
        self.fail(msg)


    def testDraw_should_clear_hidden_buffer(self):
        width, height = 20, 10
        world = World()
        world.backColor = (0.9, 0.8, 0.7, 1.0)
        win = Window(width=width, height=height)
        try:
            camera = Camera(world, win)

            camera.draw()

            rgbs = getRgbArray(win, GL_BACK)
            expectedRgb = floats_to_ubytes(world.backColor[:3])
            self.assertRgbArrayIsEntirely(rgbs, expectedRgb,
                "draw should clear to backColor")
        finally:
            win.close()


    def testDraw_should_render_the_room_color(self):
        width, height = 20, 10
        world = World()
        world.populate()
        win = Window(width=width, height=height)
        try:
            camera = Camera(world, win)
            win.dispatch_events()

            camera.draw()

            rgbs = getRgbArray(win, GL_BACK)
            expectedRgb = floats_to_ubytes(world.backColor[:3])
            self.assertRgbArrayContains(rgbs, expectedRgb,
                "should contain some backColor")

            room = [room for room in world.rooms][0]
            expectedRgb = floats_to_ubytes(room.color)
            self.assertRgbArrayContains(rgbs, expectedRgb,
                "should draw some room color")
        finally:
            win.close()


    def testDraw_should_render_rooms_correctly(self):
        width, height = 100, 100
        world = World()
        color = (0.0, 1.0, 0.0)
        verts = [(-10, -20), (-10, -30), (-30, -30), (-30, -20)]
        world.rooms = set([Room(color, verts)])
        win = Window(width=width, height=height)
        try:
            camera = Camera(world, win)
            win.dispatch_events()

            camera.draw()

            self.fail("test not complete")

        finally:
            win.close()


if __name__ == "__main__":
    run_test()

