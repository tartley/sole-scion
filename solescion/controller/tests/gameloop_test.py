#!/usr/bin/python -O
from __future__ import division

import fixpath

from pyglet import clock
from pyglet.window import key, Window

from solescion.testutils.listener import Listener
from solescion.testutils.testcase import combine, MyTestCase, run

from solescion.controller.gameloop import FPS_LIMIT, Gameloop
from solescion.controller.keyboard import Keyboard, on_key_press
from solescion.model.world import World
from solescion.view.camera import Camera
from solescion.view.renderer import Renderer


class Mock(object):
    pass


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
        self.assertEquals(Gameloop.instance, self.gameloop, "bad instance")
        self.assertNone(self.gameloop.window, "bad window")
        self.assertNone(self.gameloop.world, "bad world")
        self.assertNone(self.gameloop.camera, "bad camera")
        self.assertNone(self.gameloop.renderer, "bad renderer")


    def test_constructor_registers_handlers(self):
        expectedKeys = set([
            key.ESCAPE,
            key.PAUSE,
            key.F12,
        ])
        self.assertEquals(set(Keyboard.handlers.keys()), expectedKeys,
            "bad keys")

        expectedHandlers = [
            self.gameloop.toggle_pause,
            self.gameloop.quit_game,
        ]
        for handler in expectedHandlers:
            self.assertTrue(handler in Keyboard.handlers.values(),
                "%s not in handlers" % handler)


    def test_init_sets_fps_limit(self):
        self.gameloop.init("Gameloop.test_init_sets_fps_limit")

        self.assertEquals(clock.get_fps_limit(), float(FPS_LIMIT),
            "bad fpslimit")


    def test_init_creates_window(self):
        self.gameloop.init("Gameloop.test_init_creates_window")
        window = self.gameloop.window
        self.assertFalse(window.visible, "window should be not visible")
        self.assertTrue(window.fullscreen, "window should be fullscreen")
        self.assertTrue(window.vsync, "window should be vsync")
        self.assertEquals(window.caption,
            "Gameloop.test_init_creates_window",
            "bad window title")
        self.assertEquals(self.gameloop.window.on_key_press, on_key_press,
            "bad key handler")


    def test_init_creates_world(self):
        self.gameloop.init("Gameloop.test_init_creates_wold")
        world = self.gameloop.world
        self.assertEquals(type(world), World, "should create world")
        self.assertTrue(len(world.rooms) >= 1, "should create a room")
        self.assertTrue(len(world.chunks) > 0, "should create some chunks")


    def test_init_creates_camera(self):
        self.gameloop.init("Gameloop.test_init_creates_camera")
        camera = self.gameloop.camera
        self.assertEquals(type(camera), Camera, "should create camera")


    def test_init_creates_renderer(self):
        self.gameloop.init("Gameloop.test_init_creates_renderer")
        renderer = self.gameloop.renderer
        self.assertEquals(type(renderer), Renderer,
            "should create renderer")
        self.assertEquals(renderer.camera, self.gameloop.camera,
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
        self.assertEquals(listener.args_list, expected,
            "should call some fns")


    def test_run_skips_world_tick_when_paused(self):

        def and_quit():
            self.gameloop.window.has_exit = True

        self.gameloop.world = Mock()
        self.gameloop.world.tick = Listener()
        self.gameloop.window = Mock()
        self.gameloop.window.set_visible = lambda: None
        self.gameloop.window.dispatch_events = lambda: None
        self.gameloop.window.close = lambda: None
        self.gameloop.window.has_exit = False
        self.gameloop.window.flip = and_quit
        self.gameloop.paused = True

        self.gameloop.run()

        self.assertFalse(self.gameloop.world.tick.triggered, "not paused")


    def test_toggle_pause(self):
        self.gameloop.toggle_pause()
        self.assertTrue(self.gameloop.paused, "didn't pause")
        self.gameloop.toggle_pause()
        self.assertFalse(self.gameloop.paused, "didn't unpause")


    def test_quit(self):
        self.gameloop.window = Mock()
        self.gameloop.window.close = lambda: None
        self.gameloop.window.has_exit = False
        self.gameloop.quit_game()
        self.assertTrue(self.gameloop.window.has_exit, "window not closed")


Gameloop_test = combine(
    Gameloop_test_with_window,
    Gameloop_test_without,
)

if __name__ == "__main__":
    run(Gameloop_test)

