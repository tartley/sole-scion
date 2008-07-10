from pyglet import clock
from pyglet.gl import glClear, glClearColor, GL_COLOR_BUFFER_BIT


class Renderer(object):

    def __init__(self, window):
        self.window = window
        self.clockDisplay = clock.ClockDisplay()
        self.clearColor = (0.0, 0.0, 1.0, 1.0)


    def draw(self):
        glClearColor(*self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT)
        self.clockDisplay.draw()

