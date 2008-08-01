#!/usr/bin/python -O
from math import pi, sqrt

from pyglet.image import get_buffer_manager
from pyglet.window import Window
from pyglet.gl import (
    glBegin, glClear, glClearColor, glColor3ub, glEnd, glGetFloatv,
    glReadBuffer, glReadPixels, glVertex2f,
    GLfloat, GLubyte,
    GL_BACK, GL_COLOR_BUFFER_BIT, GL_COLOR_CLEAR_VALUE, GL_FRONT,
    GL_TRIANGLE_FAN, GL_TRIANGLES, GL_RGB, GL_UNSIGNED_BYTE,
)

import fixpath

from testutils.testimage import (
    assert_entirely, assert_contains, assert_rectangle_at, image_from_window,
    save_to_tempfile,
)
from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from model.world import Room, World
from view.camera import Camera


window = Window(
    visible=False,
    caption="Camera test",
)

class Camera_test(MyTestCase):

    def setUp(self):
        global window
        window = window
        window.set_size(200, 100)
        window.dispatch_events()
        glClearColor(0, 0, 0, 1)
        window.clear()
        self.world = World()
        self.camera = Camera(self.world, window)


    def test_constructor(self):
        global window
        self.assertTrue(self.camera.world is self.world, "should store world")
        self.assertTrue(self.camera.window is window, "should store win")
        self.assertEquals(self.camera.x, 0.0, "should init x")
        self.assertEquals(self.camera.y, 0.0, "should init y")
        self.assertEquals(self.camera.scale, 1.0, "should init scale")
        self.assertEquals(self.camera.rot, 0.0, "should init rot")


    def test_clear_fills_back_buffer_with_color(self):
        global window
        window.dispatch_events()
        color = (100, 150, 200)
        self.camera.clear(color)
        image = image_from_window(window)
        assert_entirely(image, color, "should fill with given color")


    def test_draw_clears_with_world_backColor(self):
        self.camera.clear = Listener()
        self.world.backColor = (111, 22, 3)
        self.camera.draw()
        self.assertEquals(self.camera.clear.args, ((111, 22, 3),),
            "clear not called correctly")


    def _draw_rect(self, backColor, polyColor, left, bottom, right, top):
        glClearColor(
            backColor[0]/255,
            backColor[1]/255,
            backColor[2]/255,
            1.0)
        window.clear()

        verts = [
            (left, bottom),
            (right, bottom),
            (right, top),
            (left, top),
        ]
        glColor3ub(*polyColor)
        glBegin(GL_TRIANGLE_FAN)
        for vert in verts:
            glVertex2f(*vert)
        glEnd()


    def assert_world_projection(self, drawnRect, expectedRect):
        global window

        self.camera.world_projection()

        backColor = (0, 0, 255)
        polyColor = (255, 255, 0)
        self._draw_rect(backColor, polyColor, *drawnRect)
        image = image_from_window(window)
        left, bottom, right, top = expectedRect
        assert_rectangle_at(
            image,
            left, bottom, right, top,
            polyColor, backColor)


    def test_world_projection_default(self):
        rect = (-0.2, -0.4, +0.6, +0.8)
        expectedRect = (90, 10, 129, 69)
        # note that expectedRect has y-axis inverted
        # to convert from OpenGL to PIL Image.
        self.assert_world_projection(rect, expectedRect)


    def test_defect_pyglet_get_color_buffer_for_resized_windows(self):
        window.set_size(100, 200)
        mgr = get_buffer_manager()
        window.switch_to()
        col_buf = mgr.get_color_buffer()
        col_buf_size = col_buf.width, col_buf.height
        self.assertEquals(col_buf_size, (200, 100), \
            "pyglet bug has been fixed. Enable the test below")


    # disabled due to pyglet bug: get_color_buffer() for resized window
    # returns a buffer of the old window size.
    def DONTtest_world_projection_strange_aspect(self):
        global window
        window.set_size(100, 200)
        window.dispatch_events()
        rect = (-0.2, -0.4, +0.6, +0.8)
        expectedRect = (40, 60, 79, 119)
        self.fail("get_color_buffer() for resized windows is broke"
            "fixed in pyglet subversion. expect this test to star.")
        self.assert_world_projection(rect, expectedRect)


    def test_world_projection_offset(self):
        self.camera.x, self.camera.y = (+0.5, +0.3)
        rect = (-0.2, -0.4, +0.6, +0.8)
        expectedRect = (65, 25, 104, 84)
        self.assert_world_projection(rect, expectedRect)


    def test_world_projection_scale(self):
        self.camera.scale = 10
        rect = (-1, -2, +3, +4)
        expectedRect = (95, 30, 114, 59)
        self.assert_world_projection(rect, expectedRect)


    def test_world_projection_rot(self):
        self.camera.rot = pi/2
        rect = (-0.2, -0.4, +0.6, +0.8)
        expectedRect = (60, 20, 119, 59)
        self.assert_world_projection(rect, expectedRect)


    def test_world_projection_complicated(self):
        self.camera.rot = -pi/2
        self.camera.scale = 10
        self.camera.x, self.camera.y = (5, 6)
        rect = (-1, -2, +3, +4)
        expectedRect = (60, 20, 89, 39)
        self.assert_world_projection(rect, expectedRect)


    def test_hud_projection(self):
        self.fail("write test")

    def test_draw_hud(self):
        self.fail("write test")

    def test_draw_calls_subroutines_in_right_order(self):
        self.fail("write test")


if __name__ == "__main__":
    run_test()

