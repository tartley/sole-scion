#!/usr/bin/python -O
from pyglet.window import Window

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test
from testutils.testimage import assert_entirely, image_from_window

from model.world import Entity, Room, World
from model.shapes.disc import Disc

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
        camera = Camera()
        renderer = Renderer(camera)

        roomColor = (255,0,0)
        verts = [(0,1), (1,2), (3,4)]
        room1 = Room(roomColor, verts)
        room2 = Room(roomColor, verts)

        disc = Disc(1, 0, 0)
        ent1 = Entity(disc, 1, 2, 3)
        ent2 = Entity(disc, 1, 2, 3)

        world = World()
        world.backColor = (111, 22, 3)
        world.rooms = set([room1, room2])
        world.entities = set([ent1, ent2])

        listener = Listener()
        renderer.clear = lambda *args: listener("clear", *args)
        camera.world_projection = lambda *args: listener("world_proj", *args)
        renderer.draw_room = lambda *args: listener("draw_room", *args)
        renderer.draw_entity = lambda *args: listener("draw_entity", *args)

        aspect = 1.5
        renderer.draw(world, aspect)

        expected = [
            ("clear", world.backColor),
            ("world_proj", aspect),
            ("draw_room", room2),
            ("draw_room", room1),
            ("draw_entity", ent2),
            ("draw_entity", ent1),
        ]
        self.assertEquals(listener.argsList, expected, "draw didnt call subfns")


    def test_clear_fills_back_buffer_with_color(self):
        self.window = Window(width=20, height=10, visible=False)
        self.window.dispatch_events()
        color = (100, 150, 200)
        renderer = Renderer(None)

        renderer.clear(color)

        image = image_from_window(self.window)
        assert_entirely(image, color, "should fill with given color")


    def test_draw_room(self):
        self.fail("not tested")


    def test_draw_entity(self):
        self.fail("not tested")
        self.fail("TODO: set and restore modelview projection")


if __name__ == "__main__":
    run_test(Renderer_test)
