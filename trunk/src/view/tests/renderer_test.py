#!/usr/bin/python -O
from pyglet.window import Window

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test
from testutils.testimage import assert_entirely, image_from_window

from model.world import World

from view.camera import Camera
from view.renderer import Renderer


class Renderer_test(MyTestCase):

    def setUp(self):
        self.window = None

    def tearDown(self):
        if self.window:
            self.window.close()


    def test_constructor(self):
        camera = object()
        renderer = Renderer(camera)
        self.assertEquals(renderer.camera, camera, "should store camera")


    def test_draw_calls_subroutines_in_right_order(self):
        listener = Listener()
        camera = Camera()
        renderer = Renderer(camera)
        world = World()
        renderer.clear = lambda *_: listener("clear")
        camera.world_projection = lambda *_: listener("world_projection")
        renderer.draw_world = lambda *_: listener("draw_world")

        renderer.draw(world, 1.5)

        expected = [
            ("clear",),
            ("world_projection",),
            ("draw_world",),
        ]
        self.assertEquals(listener.argsList, expected, "draw didnt call subfns")


    def test_draw_clears_with_world_backColor(self):
        camera = Camera()
        world = World()
        world.backColor = (111, 22, 3)
        renderer = Renderer(camera)
        renderer.clear = Listener()

        renderer.draw(world, 1.5)

        self.assertEquals(renderer.clear.args, ((111, 22, 3),),
            "clear not called correctly")


    def test_clear_fills_back_buffer_with_color(self):
        self.window = Window(width=20, height=10, visible=False)
        self.window.dispatch_events()
        color = (100, 150, 200)
        renderer = Renderer(None)

        renderer.clear(color)

        image = image_from_window(self.window)
        assert_entirely(image, color, "should fill with given color")


if __name__ == "__main__":
    run_test(Renderer_test)

