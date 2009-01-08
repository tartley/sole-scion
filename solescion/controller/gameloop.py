from __future__ import division

from pyglet import clock
from pyglet.window import key, Window

from solescion.controller.keyboard import Keyboard, on_key_press
from solescion.model.world import World
from solescion.utils.screenshot import save_screenshot
from solescion.view.camera import Camera
from solescion.view.renderer import Renderer


FPS_LIMIT = 60


class Gameloop(object):

    instance = None

    def __init__(self):
        Gameloop.instance = self
        self.window = None
        self.camera = None
        self.world = None
        self.renderer = None
        self.paused = False
        Keyboard.handlers.update({
            key.ESCAPE: self.quit_game,
            key.PAUSE: self.toggle_pause,
            key.F12: lambda: save_screenshot(self.window),
        })


    def init(self, caption):
        clock.set_fps_limit(FPS_LIMIT)
        self.world = World()
        self.world.populate()
        self.camera = Camera((0, 0), 50)
        self.renderer = Renderer(self.camera)
        self.window = Window(
            caption=caption, fullscreen=True, visible=False)
        self.window.on_key_press = on_key_press
        self.window.push_handlers(Keyboard.keystate)


    def dispose(self):
        if self.window:
            self.window.close()


    def run(self):
        try:
            self.window.set_visible()
            while not self.window.has_exit:
                self.window.dispatch_events()
                clock.tick()
                if self.world and not self.paused:
                    self.world.tick(1/FPS_LIMIT)
                if self.world and hasattr(self.world, 'player'):
                    self.camera.x, self.camera.y = \
                        self.world.player.chunks[0].body.position
                if self.renderer:
                    aspect = (
                        self.window.width / self.window.height)
                    self.renderer.draw(self.world, aspect)
                self.window.flip()
        finally:
            self.dispose()


    def toggle_pause(self):
        self.paused = not self.paused


    def quit_game(self):
        self.window.has_exit = True

