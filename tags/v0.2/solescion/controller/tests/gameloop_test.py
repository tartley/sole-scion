#!/usr/bin/python -O
from __future__ import division
from pyglet import clock
from pyglet.window import Window

import fixpath

from testutils.testcase import MyTestCase, run_test

from controller.gameloop import Gameloop
from model.world import World
from view.camera import Camera
from view.renderer import Renderer


class Gameloop_test(MyTestCase):

    def setUp(self):
        self.gameloop = Gameloop("Gameloop.setUp")


    def tearDown(self):
        self.gameloop.dispose()


    def test_constructor(self):
        self.assertEquals(self.gameloop.fpsLimit, 30,
            "should define fps_limit")
        self.assertEquals(clock.get_fps_limit(), 30.0,
            "should set fps limit")
        self.assertEquals(self.gameloop.deltaT, None,
            "should set current frame time")
        self.assertEquals(self.gameloop.ticks, [], "should set ticks")

        self.assertEquals(type(self.gameloop.world), World,
            "should create world")
        self.assertEquals(len(self.gameloop.world.rooms), 1,
            "should create world with one room")

        self.assertEquals(type(self.gameloop.window), Window,
            "should create window")
        self.assertFalse(self.gameloop.window.visible,
            "window should be not visible")
        self.assertTrue(self.gameloop.window.fullscreen,
            "window should be fullscreen")
        self.assertTrue(self.gameloop.window.vsync,
            "window should be vsync")
        self.assertEquals(type(self.gameloop.camera), Camera,
            "should create camera")

        self.assertEquals(type(self.gameloop.renderer), Renderer,
            "should create renderer")
        self.assertEquals(self.gameloop.renderer.camera, self.gameloop.camera,
            "should create renderer with camera")


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


    def test_run_sets_deltaT(self):
        def setHasExit():
            self.gameloop.window.has_exit = True

        self.gameloop.window.flip = setHasExit

        import controller.gameloop as gameloopModule
        oldTick = gameloopModule.clock.tick
        gameloopModule.clock.tick = lambda: 12345
        try:
            self.gameloop.run()
        finally:
            gameloopModule.clock.tick = oldTick

        self.assertEquals(self.gameloop.deltaT, 12345,
            "run should assign deltaT=clock.tick")
        self.assertEquals(self.gameloop.ticks, [12345],
            "run should append deltaT to ticks")


    def test_run_calls_some_functions(self):
        calls = []

        def recordCall(*args):
            calls.append(args)
            self.gameloop.window.has_exit = True

        self.gameloop.window.dispatch_events = \
            lambda *args: recordCall("dispatch", args)
        self.gameloop.world.tick = \
            lambda *args: recordCall("tick", args)
        self.gameloop.renderer.draw = \
            lambda *args: recordCall("draw", args)
        self.gameloop.window.flip = \
            lambda *args: recordCall("flip", args)

        self.gameloop.run()

        win = self.gameloop.window
        aspect = win.width / win.height
        expected = [
            ('dispatch', ()),
            ('tick', (1/30,)),
            ('draw', (self.gameloop.world, aspect)),
            ('flip', ()),
        ]
        self.assertEquals(calls, expected, "run should call some functions")


    def test_run_closes_the_window_on_exception(self):

        self.closeCalled = False
        origClose = self.gameloop.window.close

        def raisePlease():
            raise ZeroDivisionError("msg")

        def closeWindow():
            self.closeCalled = True
            self.gameloop.window.close = origClose
            self.gameloop.window.close()

        self.gameloop.window.dispatch_events = raisePlease
        self.gameloop.window.close = closeWindow
        self.assertRaises(
            self.gameloop.run,
            ZeroDivisionError,
            "msg")
        self.assertTrue(self.closeCalled, "window should be closed")


if __name__ == "__main__":
    run_test(Gameloop_test)

