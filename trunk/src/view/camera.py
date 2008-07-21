from pyglet import clock
from pyglet.gl import (
    glBegin, glClear, glClearColor, glColor3f, glEnd, glLoadIdentity,
    glVertex2f,
    GL_COLOR_BUFFER_BIT, GL_TRIANGLE_FAN,
)


class Camera(object):

    def __init__(self, world, window):
        self.world = world
        self.window = window
        self.clockDisplay = clock.ClockDisplay()


    def draw(self):
        glClearColor(*self.world.backColor)
        glClear(GL_COLOR_BUFFER_BIT)

        glLoadIdentity()
        for room in self.world.rooms:
            glColor3f(*room.color)
            glBegin(GL_TRIANGLE_FAN)
            for vert in room.verts:
                glVertex2f(*vert)
            glEnd()

        self.clockDisplay.draw()
