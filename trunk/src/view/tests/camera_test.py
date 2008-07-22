#!/usr/bin/python -O
from math import pi, sqrt

from pyglet.window import Window
from pyglet.gl import (
    glClear, glClearColor, glGetFloatv, glReadBuffer, glReadPixels,
    GLfloat, GLubyte,
    GL_BACK, GL_COLOR_BUFFER_BIT, GL_COLOR_CLEAR_VALUE, GL_FRONT, GL_RGB,
    GL_UNSIGNED_BYTE,
)

import fixpath

from testutils.testcase import MyTestCase, run_test

from model.world import Room, World
from view.camera import Camera


class Image(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        numBytes = width * height * 3
        self.pixeldata = (GLubyte * numBytes)(*(0 for _ in range(numBytes)))

    @staticmethod
    def from_buffer(win, buff=GL_FRONT):
        image = Image(win.width, win.height)
        glReadBuffer(buff)
        glReadPixels(
            0, 0, image.width, image.height,
            GL_RGB, GL_UNSIGNED_BYTE, image.pixeldata)
        return image


    def get_pixel(self, x, y):
        if 0 > x >= self.width or 0 > y >= self.height:
            msg = "%s,%s out of range. image=%s,%s" % \
                (x, y, self.width, self.height)
            raise AssertionError(msg)
        idx = (x + y * self.width) * 3
        return tuple(self.pixeldata[idx:idx+3])


    def assert_entirely(self, expectedRgb, assertMsg=None):
        for idx in range(0, len(self.pixeldata), 3):
            rgb = tuple(self.pixeldata[idx:idx+3])
            if rgb != expectedRgb:
                msg = "%s != %s\n  pixel %d wrong color\n  %s" % \
                    (rgb, expectedRgb, idx, assertMsg)
                raise AssertionError(msg)


    def assert_contains(self, expectedRgb, assertMsg=None):
        found = set()
        for idx in range(0, len(self.pixeldata), 3):
            rgb = tuple(self.pixeldata[idx:idx+3])
            found.add(rgb)
            if rgb == expectedRgb:
                return
        msg = "did not contain %s\ndid contain: %s\n%s" % \
            (expectedRgb, found, assertMsg)
        raise AssertionError(msg)


    def assert_rectangle_at(self, left, bottom, right, top, rectCol, backCol):
        badPixels = []

        # inside rect is rectcol
        if self.get_pixel(left+1, bottom+1) != rectCol:
            badPixels += ["bottom left"]
        if self.get_pixel(right-1, bottom+1) != rectCol:
            badPixels += ["bottom right"]
        if self.get_pixel(left+1, top-1) != rectCol:
            badPixels += ["top left"]
        if self.get_pixel(right-1, top-1) != rectCol:
            badPixels += ["top right"]

        # outside rect is backCol
        if self.get_pixel(left-1, bottom+1) != backCol:
            badPixels += ["bottom left, left edge"]
        if self.get_pixel(left+1, bottom-1) != backCol:
            badPixels += ["bottom left, bottom edge"]
        if self.get_pixel(right+1, bottom+1) != backCol:
            badPixels += ["bottom right, right edge"]
        if self.get_pixel(right-1, bottom-1) != backCol:
            badPixels += ["bottom right, bottom edge"]
        if self.get_pixel(left-1, top-1) != backCol:
            badPixels += ["top left, left edge"]
        if self.get_pixel(left+1, top+1) != backCol:
            badPixels += ["top left, top edge"]
        if self.get_pixel(right+1, top-1) != backCol:
            badPixels += ["top right, right edge"]
        if self.get_pixel(right-1, top+1) != backCol:
            badPixels += ["top right, top edge"]

        if badPixels:
            raise AssertionError('bad pixels at:\n  ' + '\n  '.join(badPixels))


class Camera_test(MyTestCase):

    def setup(self):
        self.world = World()


    def testConstructor(self):
        world = World()
        window = Window(width=200, height=100, caption="Camera.testConstructor")
        try:
            camera = Camera(world, window, 123.0)
            self.assertTrue(camera.world is world, "should store model")
            self.assertTrue(camera.window is window, "should store window")
            self.assertEquals(camera.scale, 123.0, "should store scale")
        finally:
            window.close()


    def testDraw_should_clear_buffer_with_world_backcolor(self):
        world = World()
        world.backColor = (250, 100, 150)
        win = Window(width=200, height=100, caption="Camera.testDraw_scbwwb")
        try:
            win.dispatch_events()
            camera = Camera(world, win, 1)

            camera.draw()
            win.flip()

            image = Image.from_buffer(win)
            image.assert_entirely(world.backColor, "should clear to backColor")
        finally:
            win.close()


    def testDraw_should_draw_the_room_color(self):
        verts = [(-10, -10), (-10, +10), (+10, 0)]
        room = Room((150, 100, 50), verts)
        world = World()
        world.rooms = set([room])
        win = Window(width=200, height=100, caption="Camera.testDraw_sdtrc")
        try:
            win.dispatch_events()
            camera = Camera(world, win, 10)

            camera.draw()
            win.flip()

            image = Image.from_buffer(win)
            image.assert_contains(room.color, "should draw some room color")
        finally:
            win.close()


    def assert_room_drawn(self, verts,
        camFocus, camScale, camRot,
        expectedEdges):

        world = World()
        room = Room((255, 255, 0), verts)
        world.rooms = set([room])
        win = Window(width=200, height=100,
            caption="Camera.assert_room_drawn")
        try:
            win.dispatch_events()
            camera = Camera(world, win, camScale)
            camera.x, camera.y = camFocus
            camera.rot = camRot

            camera.draw()
            win.flip()

            image = Image.from_buffer(win)
            left = win.width/2 + expectedEdges[0]
            bottom = win.height/2 + expectedEdges[1]
            right = win.width/2 + expectedEdges[2]
            top = win.height/2 + expectedEdges[3]
            image.assert_rectangle_at(
                left, bottom, right, top,
                room.color, world.backColor)
        finally:
            win.close()


    def testDraw_xforms_room_verts_by_camera_scale(self):
        roomVerts = [(-20, -10), (-20, 30), (40, 30), (40, -10)]
        camScale = 50
        expectedEdges = [-20, -10, +40, +30]
        self.assert_room_drawn(
            roomVerts,
            (0, 0), camScale, 0,
            expectedEdges)


    def testDraw_xforms_room_verts_by_cam_scale_and_xy(self):
        roomVerts = [(-20, -10), (-20, 30), (40, 30), (40, -10)]
        camFocus = 40, 30
        camScale = 100
        expectedEdges = [-30, -20, 0, 0]
        self.assert_room_drawn(
            roomVerts,
            camFocus, camScale, 0,
            expectedEdges)


    def testDraw_xforms_room_verts_by_cam_scale_xy_and_rot(self):
        r2 = sqrt(2) * 10
        roomVerts = [
            (+40 -5*r2, +30 +r2),
            (+40 -3*r2, +30 +3*r2),
            (+40 +0,    +30 +0),
            (+40 -2*r2, +30 -2*r2)]
        camFocus = 40, 30
        camScale = 100
        camRot = pi/4
        expectedEdges = [-30, -20, 0, 0]
        self.assert_room_drawn(
            roomVerts,
            camFocus, camScale, camRot,
            expectedEdges)


if __name__ == "__main__":
    run_test()

