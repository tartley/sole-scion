from __future__ import division

from pyglet import clock
from pyglet.window import Window

from model.world import World
from view.camera import Camera
from view.renderer import Renderer


class Gameloop(object):

    def __init__(self, caption):
        self.fpsLimit = 30
        clock.set_fps_limit(self.fpsLimit)
        self.deltaT = None
        self.ticks = []
        self.world = World()
        self.world.populate()
        self.window = Window( \
            fullscreen=True, vsync=True, caption=caption, visible=False)
        self.camera = Camera()
        self.camera.scale = 8
        self.camera.x, self.camera.y = (0, 5)
        self.renderer = Renderer(self.camera)


    def dispose(self):
        self.window.close()


    def run(self):
        self.window.set_visible(True)
        try:
            while not self.window.has_exit:
                self.deltaT = clock.tick()
                self.ticks.append(self.deltaT)
                self.window.dispatch_events()
                self.world.tick(1/self.fpsLimit)
                aspect = self.window.width / self.window.height
                self.renderer.draw(self.world, aspect)
                self.window.flip()
        finally:
            self.dispose()

