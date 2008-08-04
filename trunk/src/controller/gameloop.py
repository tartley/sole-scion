from pyglet import clock
from pyglet.window import Window

from model.world import World
from view.camera import Camera
from view.renderer import Renderer


class Gameloop(object):

    def __init__(self, caption):
        self.fps_limit = 30
        clock.set_fps_limit(self.fps_limit)
        self.dt = None
        self.ticks = []
        self.world = World()
        self.world.populate()
        self.window = Window( \
            fullscreen=True, vsync=True, caption=caption, visible=False)
        self.camera = Camera()
        self.renderer = Renderer(self.camera)


    def dispose(self):
        self.window.close()


    def run(self):
        self.window.set_visible(True)
        try:
            while not self.window.has_exit:
                self.dt = clock.tick()
                self.ticks.append(self.dt)
                self.window.dispatch_events()
                aspect = self.window.width / self.window.height
                self.renderer.draw(self.world, aspect)
                self.window.flip()
        finally:
            self.dispose()

