"""
Top level gameloop that cycles throughout the entire lifetime of the
application.
"""
from pyglet import clock
from pyglet.window import Window

from model.world import World
from view.camera import Camera
from view.renderer import Renderer


class Gameloop(object):
    """Sole class of the 'gameloop' module"""

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
        self.renderer = Renderer(self.camera)


    def dispose(self):
        """Disposes of resources created in __init__"""
        self.window.close()


    def run(self):
        """Program's main animation loop"""
        self.window.set_visible(True)
        try:
            while not self.window.has_exit:
                self.deltaT = clock.tick()
                self.ticks.append(self.deltaT)
                self.window.dispatch_events()
                aspect = self.window.width / self.window.height
                self.renderer.draw(self.world, aspect)
                self.window.flip()
        finally:
            self.dispose()

