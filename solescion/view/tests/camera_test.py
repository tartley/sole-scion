#!/usr/bin/python -O
from __future__ import division
from math import pi

from pyglet.image import get_buffer_manager
from pyglet.window import Window
from pyglet.gl import (
    glBegin, glClearColor, glColor3ub, glEnd, glVertex2f,
    GL_TRIANGLE_FAN,
)

import fixpath

from solescion.testutils.testimage import assert_rectangle_at
from solescion.testutils.testcase import MyTestCase, run

from solescion.model.world import World
from solescion.utils.screenshot import image_from_window
from solescion.view.camera import Camera


class Camera_test(MyTestCase):

    def setUp(self):
        self.window = Window(
            width=200, height=100, visible=False, caption="Camera_test setup")
        self.window.dispatch_events()
        glClearColor(0, 0, 0, 1)
        self.window.clear()
        self.world = World()
        self.camera = Camera((0, 0), 1)


    def tearDown(self):
        self.window.close()


    def test_constructor(self):
        camera = Camera((1, 2), 3, 4)
        self.assertEquals(camera.x, 1, "should init x")
        self.assertEquals(camera.y, 2, "should init y")
        self.assertEquals(camera.scale, 3, "should init scale")
        self.assertEquals(camera.angle, 4, "should init angle")


    def test_constructor_defaults_angle(self):
        camera = Camera((10, 20), 30)
        self.assertEquals(camera.angle, 0.0, "should init angle")


    def _draw_rect(self, backColor, polyColor, left, bottom, right, top):
        glClearColor(
            backColor[0]/255,
            backColor[1]/255,
            backColor[2]/255,
            1.0)
        self.window.clear()

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
        # Python Imaging Library Image object measures Y from top,
        # so expectedRect has y-axis inverted
        left, bottom, right, top = expectedRect
        expectedRect = left, bottom, right, top
        aspect = self.window.width / self.window.height
        self.camera.world_projection(aspect)

        backColor = (0, 0, 255)
        polyColor = (255, 255, 0)
        self._draw_rect(backColor, polyColor, *drawnRect)
        image = image_from_window(self.window)
        # expectedRect[1] = self.window.height - expectedRect[3] - 1
        # expectedRect[2] = expectedRect[2] - 1
        # expectedRect[3] = self.window.height - expectedRect[1]
        assert_rectangle_at(image, expectedRect, polyColor, backColor)


    def test_world_projection_default(self):
        rect = (-0.2, -0.4, +0.6, +0.8)
        expectedRect = (90, 10, 129, 69)
        self.assert_world_projection(rect, expectedRect)


    def test_defect_pyglet_get_color_buffer_for_resized_windows(self):
        self.window.set_size(111, 222)
        self.window.dispatch_events()
        mgr = get_buffer_manager()
        col_buf = mgr.get_color_buffer()
        col_buf_size = col_buf.width, col_buf.height
        self.assertEquals(col_buf_size, (111, 222), "pyglet bug regression")


    def test_world_projection_strange_aspect(self):
        # create a new window, since
        # resizing the existing window doesn't work for some reason
        # even if we dispatch events. Default handlers?
        self.window.close()
        self.window = Window(
            width=100, height=200, visible=False,
            caption="world.test_projection_strange_aspect")
        self.window.dispatch_events()
        rect = (-0.2, -0.4, +0.6, +0.8)
        expectedRect = (40, 60, 79, 119)
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


    def test_world_projection_angle(self):
        self.camera.angle = pi/2
        rect = (-0.2, -0.4, +0.6, +0.8)
        expectedRect = (60, 20, 119, 59)
        self.assert_world_projection(rect, expectedRect)


    def test_world_projection_complicated(self):
        self.camera.angle = -pi/2
        self.camera.scale = 10
        self.camera.x, self.camera.y = (5, 6)
        rect = (-1, -2, +3, +4)
        expectedRect = (60, 20, 89, 39)
        self.assert_world_projection(rect, expectedRect)



if __name__ == "__main__":
    run(Camera_test)

