from pyglet import clock
from pyglet.gl import *


class Renderer(object):

    def __init__(self, window):
        self.window = window
        glClearColor(0.0, 0.0, 1.0, 1.0)
        self.clockDisplay = clock.ClockDisplay()


    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.clockDisplay.draw()

