#!/usr/bin/python -O
from pyglet.window import key, Window

import fixpath

from solescion.testutils.listener import Listener
from solescion.testutils.testcase import MyTestCase, run
from solescion.testutils.testimage import assert_entirely

from solescion.model.world import Chunk, Room, World
from solescion.model.shards.disc import Disc
from solescion.utils.screenshot import image_from_window

from solescion.view.camera import Camera
from solescion.view.renderer import Renderer


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
        camera = Camera((0, 1), 2)
        renderer = Renderer(camera)

        roomColor = (255,0,0)
        verts = [(-1, 0), (2,3), (4, 0)]
        room1 = Room(verts)
        room2 = Room(verts)

        chunk1 = Chunk()
        chunk2 = Chunk()

        world = World()
        world.backColor = (111, 22, 3)
        world.rooms = {1: room1, 2: room2}
        world.chunks = set([chunk1, chunk2])

        listener = Listener()
        renderer.clear = \
            lambda *args: listener("clear", *args)
        camera.world_projection = \
            lambda *args: listener("world_proj", *args)
        renderer.draw_rooms = \
            lambda *args: listener("draw_rooms", *args)
        renderer.draw_chunk = \
            lambda *args: listener("draw_chunk", *args)

        aspect = 1.5
        renderer.draw(world, aspect)

        expected = [
            ("clear", world.material.color),
            ("world_proj", aspect),
            ("draw_rooms", {1: room1, 2: room2}),
            ("draw_chunk", chunk1),
            ("draw_chunk", chunk2),
        ]
        self.assertEquals(listener.args_list, expected,
            "draw didnt call subfns")


    def test_clear_fills_back_buffer_with_color(self):
        self.window = Window(
            width=20, height=10, visible=False,
            caption="renderer.test_clear_fills_back_buffer_with_color")
        self.window.dispatch_events()
        color = (100, 150, 200)
        renderer = Renderer(None)

        renderer.clear(color)

        image = image_from_window(self.window)
        assert_entirely(image, color, "should fill with given color")


if __name__ == "__main__":
    run(Renderer_test)

