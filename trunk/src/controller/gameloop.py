from pyglet import clock
from pyglet.window import Window

from view.renderer import Renderer


class Gameloop(object):

    def __init__(self):
        self.fps_limit = 30
        clock.set_fps_limit(self.fps_limit)
        self.dt = None
        self.ticks = []
        self.window = Window(fullscreen=True, vsync=True)
        self.renderer = Renderer(self.window)


    def run(self):
        while not self.window.has_exit:
            self.dt = clock.tick()
            self.ticks.append(self.dt)
            self.window.dispatch_events()
            self.renderer.draw()
            self.window.flip()

