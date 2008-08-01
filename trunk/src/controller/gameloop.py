from pyglet import clock
from pyglet.window import Window

from model.world import World
from view.camera import Camera


class Gameloop(object):

    def __init__(self, caption):
        self.fps_limit = 30
        clock.set_fps_limit(self.fps_limit)
        self.dt = None
        self.ticks = []
        self.world = World()
        self.world.populate()
        self.window = Window(fullscreen=True, vsync=True, caption=caption)
        self.camera = Camera(self.world, self.window)


    def dispose(self):
        self.window.close()


    def run(self):
        try:
            while not self.window.has_exit:
                self.dt = clock.tick()
                self.ticks.append(self.dt)
                self.window.dispatch_events()
                self.camera.draw()
                self.window.flip()
        finally:
            self.dispose()

