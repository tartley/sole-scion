#!/usr/bin/python -O
from __future__ import division
from pyglet import clock
from pyglet.window import Window

import fixpath

from testutils.listener import Listener
from testutils.testcase import combine, MyTestCase, run_test

from application import title
from controller.gameloop import FPS_LIMIT, Gameloop
from model.world import World
from view.camera import Camera
from view.renderer import Renderer


class Gameloop_test_with_window(MyTestCase):

    def setUp(self):
        self.gameloop = Gameloop()
        self.gameloop.window = Window(
            visible=False,
            caption="Gameloop_test")

    def tearDown(self):
        if self.gameloop.window:
            self.gameloop.window.close()


    def test_dispose(self):
        self.gameloop.dispose()
        self.assertFalse(self.gameloop.window.has_exit, "window not closed")


    def test_run_shows_window(self):
        def setHasExit():
            self.assertTrue(self.gameloop.window.visible, \
                "run should set visible=True")
            self.gameloop.window.has_exit = True
        self.gameloop.window.flip = setHasExit
        self.gameloop.run()


    def test_run_loops_until_done(self):
        calls = []
        self.callsLeft = 3

        def setHasExitOnZero():
            calls.append(self.callsLeft)
            self.callsLeft -= 1
            if self.callsLeft == 0:
                self.gameloop.window.has_exit = True

        self.gameloop.window.flip = setHasExitOnZero
        self.gameloop.run()
        self.assertEquals(calls, [3, 2, 1], "run should iterate thrice")


    def test_run_closes_the_window_on_exception(self):

        def raisePlease():
            raise ZeroDivisionError("msg")

        self.gameloop.window.dispatch_events = raisePlease
        orig = self.gameloop.window.close
        self.gameloop.window.close = Listener()
        try:
            self.assertRaises(self.gameloop.run, ZeroDivisionError, "msg")
            self.assertTrue(self.gameloop.window.close.triggered, \
                "window should be closed")
        finally:
            self.gameloop.window.close = orig



class Gameloop_test_without(MyTestCase):

    def setUp(self):
        self.gameloop = Gameloop()

    def tearDown(self):
        self.gameloop.world = None
        if self.gameloop.window:
            self.gameloop.window.close()


    def test_constructor(self):
        self.assertNone(self.gameloop.window, "bad window")
        self.assertNone(self.gameloop.world, "bad world")
        self.assertNone(self.gameloop.camera, "bad camera")
        self.assertNone(self.gameloop.renderer, "bad renderer")


    def test_dummy(self):
        self.gameloop.init("dummy")


    def test_init(self):
        self.gameloop.init("Gameloop.test_init")

        self.assertEquals(clock.get_fps_limit(), float(FPS_LIMIT),
            "bad fpslimit")

        window = self.gameloop.window
        self.assertFalse(window.visible, "window should be not visible")
        self.assertTrue(window.fullscreen, "window should be fullscreen")
        self.assertTrue(window.vsync, "window should be vsync")
        self.assertEquals(window.caption, "Gameloop.test_init",
            "bad window title")

        world = self.gameloop.world
        self.assertEquals(type(world), World, "should create world")
        self.assertEquals(len(world.rooms), 1, "should create a room")
        self.assertTrue(len(world.chunks) > 0, "should create some chunks")

        camera = self.gameloop.camera
        self.assertEquals(type(camera), Camera, "should create camera")

        renderer = self.gameloop.renderer
        self.assertEquals(type(renderer), Renderer, "should create renderer")
        self.assertEquals(renderer.camera, camera,
            "should create renderer with camera")


    def test_dispose_with_no_window(self):
        self.gameloop.dispose()


    def test_run_calls_some_functions(self):
        self.gameloop.init("Gameloop.test_run_calls_some_fns")

        def and_quit():
            self.gameloop.window.has_exit = True

        listener = Listener()
        self.gameloop.window.dispatch_events = \
            lambda *args: listener(1, *args)
        self.gameloop.world.tick = \
            lambda *args: listener(2, *args)
        self.gameloop.renderer.draw = \
            lambda *args: listener(3, *args)
        self.gameloop.window.flip = \
            lambda *args: (listener(4, *args), and_quit())

        self.gameloop.run()

        win = self.gameloop.window
        aspect = win.width / win.height
        expected = [
            (1,),
            (2, 1/FPS_LIMIT,),
            (3, self.gameloop.world, aspect),
            (4,),
        ]
        self.assertEquals(listener.argsList, expected, "should call some fns")


Gameloop_test = combine(
    Gameloop_test_with_window,
    Gameloop_test_without,
)

if __name__ == "__main__":
    run_test(Gameloop_test)

