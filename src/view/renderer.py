from pyglet import clock
from pyglet.gl import (
    glBegin, glClear, glClearColor, glColor3f, glEnd, glLoadIdentity,
    glVertex2f,
    GL_COLOR_BUFFER_BIT, GL_TRIANGLE_FAN,
)


class Renderer(object):

    def __init__(self, world, window):
        self.world = world
        self.window = window
        self.clockDisplay = clock.ClockDisplay()
        self.clearColor = (0.0, 0.0, 1.0, 1.0)


    def draw(self):
        glClearColor(*self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT)

        # TOOD: untested, mostly
        glLoadIdentity()
        for room in self.world.rooms:
            glColor3f(*room.color)
            glBegin(GL_TRIANGLE_FAN)
            for vert in room.verts:
                glVertex2f(*vert)
            glEnd()

        self.clockDisplay.draw()
