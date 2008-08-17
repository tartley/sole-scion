from __future__ import division

from pyglet import clock
from pyglet.window import Window

from model.world import World
from view.camera import Camera
from view.renderer import Renderer


FPS_LIMIT = 60

class Gameloop(object):

    def __init__(self):
        self.window = None
        self.camera = None
        self.world = None
        self.renderer = None


    def init(self, caption):
        clock.set_fps_limit(FPS_LIMIT)
        self.world = World()
        self.world.populate()
        self.camera = Camera()
        self.renderer = Renderer(self.camera)
        self.window = Window(
            caption=caption, fullscreen=True, visible=False)


    def dispose(self):
        if self.window:
            self.window.close()


    def run(self):
        try:
            self.window.set_visible()
            while not self.window.has_exit:
                self.window.dispatch_events()
                clock.tick()
                if self.world:
                    self.world.tick(1/FPS_LIMIT)
                aspect = self.window.width / self.window.height
                if self.renderer:
                    self.renderer.draw(self.world, aspect)
                self.window.flip()
        finally:
            self.dispose()

