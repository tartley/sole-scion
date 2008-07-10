from pyglet import clock
from pyglet.window import Window

import fix_pythonpath

from testutils.testcase import MyTestCase, run_test

from controller.gameloop import Gameloop
from view.renderer import Renderer


class Gameloop_test(MyTestCase):

    def testConstructor(self):
        clock.set_fps_limit(1000)
        gameloop = Gameloop()
        self.assertEquals(gameloop.fps_limit, 30, "should define fps_limit")
        self.assertEquals(clock.get_fps_limit(), 30.0, "should set fps limit")
        self.assertEquals(gameloop.dt, None, "should set current frame time")
        self.assertEquals(gameloop.ticks, [], "should set ticks")
        self.assertEquals(type(gameloop.window), Window,
            "should create window")
        self.assertTrue(gameloop.window.fullscreen,
            "window should be fullscreen")
        self.assertTrue(gameloop.window.vsync,
            "window should be vsync")
        self.assertEquals(type(gameloop.renderer), Renderer,
            "should create renderer")
        self.assertTrue(gameloop.renderer.window is gameloop.window,
            "should create renderer with our window")


    def testRunShouldLoopUntilDone(self):
        calls = []
        self.callsLeft = 3
        gameloop = Gameloop()

        def setHasExitOnZero():
            calls.append(self.callsLeft)
            self.callsLeft -= 1
            if self.callsLeft == 0:
                gameloop.window.has_exit = True

        gameloop.window.flip = setHasExitOnZero
        gameloop.run()
        self.assertEquals(calls, [3, 2, 1], "run should iterate thrice")


    def testRunShouldSetDt(self):
        gameloop = Gameloop()

        def setHasExit():
            gameloop.window.has_exit = True

        gameloop.window.flip = setHasExit

        import controller.gameloop as gameloopModule
        oldTick = gameloopModule.clock.tick
        gameloopModule.clock.tick = lambda: 12345
        try:
            gameloop.run()
        finally:
            gameloopModule.clock.tick = oldTick

        self.assertEquals(gameloop.dt, 12345,
            "run should assign dt=clock.tick")
        self.assertEquals(gameloop.ticks, [12345],
            "run should append dt to ticks")


    def testRunShouldCallSomeFunctions(self):
        gameloop = Gameloop()
        calls = []

        def recordCall(*args):
            calls.append(args)
            gameloop.window.has_exit = True

        gameloop.window.dispatch_events = \
            lambda *args: recordCall("dispatch", args)
        gameloop.renderer.draw = \
            lambda *args: recordCall("draw", args)
        gameloop.window.flip = \
            lambda *args: recordCall("flip", args)

        gameloop.run()

        expected = [
            ('dispatch', ()),
            ('draw', ()),
            ('flip', ()),
        ]
        self.assertEquals(calls, expected, "run should call some functions")


if __name__ == "__main__":
    run_test()

