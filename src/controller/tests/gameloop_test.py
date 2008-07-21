#!/usr/bin/python -O

from pyglet import clock
from pyglet.window import Window

import fixpath

from testutils.testcase import MyTestCase, run_test

from controller.gameloop import Gameloop
from model.world import World
from view.camera import Camera


class Gameloop_test(MyTestCase):

    def setUp(self):
        self.gameloop = Gameloop()


    def tearDown(self):
        self.gameloop.dispose()


    def testConstructor(self):
        self.assertEquals(self.gameloop.fps_limit, 30,
            "should define fps_limit")
        self.assertEquals(clock.get_fps_limit(), 30.0,
            "should set fps limit")
        self.assertEquals(self.gameloop.dt, None,
            "should set current frame time")
        self.assertEquals(self.gameloop.ticks, [], "should set ticks")

        self.assertEquals(type(self.gameloop.world), World,
            "should create world")
        self.assertEquals(len(self.gameloop.world.rooms), 1,
            "should create world with one room")

        self.assertEquals(type(self.gameloop.window), Window,
            "should create window")
        self.assertTrue(self.gameloop.window.fullscreen,
            "window should be fullscreen")
        self.assertTrue(self.gameloop.window.vsync,
            "window should be vsync")
        self.assertEquals(type(self.gameloop.camera), Camera,
            "should create camera")
        self.assertTrue(self.gameloop.camera.window is self.gameloop.window,
            "should create camera with our window")


    def testRunShouldLoopUntilDone(self):
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


    def testRunShouldSetDt(self):
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

        self.assertEquals(self.gameloop.dt, 12345,
            "run should assign dt=clock.tick")
        self.assertEquals(self.gameloop.ticks, [12345],
            "run should append dt to ticks")


    def testRunShouldCallSomeFunctions(self):
        calls = []

        def recordCall(*args):
            calls.append(args)
            self.gameloop.window.has_exit = True

        self.gameloop.window.dispatch_events = \
            lambda *args: recordCall("dispatch", args)
        self.gameloop.camera.draw = \
            lambda *args: recordCall("draw", args)
        self.gameloop.window.flip = \
            lambda *args: recordCall("flip", args)

        self.gameloop.run()

        expected = [
            ('dispatch', ()),
            ('draw', ()),
            ('flip', ()),
        ]
        self.assertEquals(calls, expected, "run should call some functions")


if __name__ == "__main__":
    run_test()

