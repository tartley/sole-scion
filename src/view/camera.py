from __future__ import division
from math import sin, cos

from pyglet import clock
from pyglet.gl import (
    glBegin, glClear, glClearColor, glColor3ub, glEnd, glLoadIdentity,
    glMatrixMode, glVertex2f,
    gluLookAt, gluOrtho2D, 
    GL_COLOR_BUFFER_BIT, GL_TRIANGLE_FAN, GL_MODELVIEW, GL_PROJECTION
)


class Camera(object):

    def __init__(self, world, window, scale):
        self.world = world
        self.window = window
        self.scale = scale
        self.clockDisplay = clock.ClockDisplay()
        self.x = 0.0
        self.y = 0.0
        self.rot = 0.0


    def worldProjection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = self.window.width / self.window.height
        gluOrtho2D(
            -self.scale * aspect,
            +self.scale * aspect,
            -self.scale,
            +self.scale)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            self.x, self.y, +1.0,
            self.x, self.y, -1.0,
            sin(self.rot), cos(self.rot), 0.0)


    def draw(self):
        glClearColor(
            self.world.backColor[0] / 255,
            self.world.backColor[1] / 255,
            self.world.backColor[2] / 255,
            1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.worldProjection()
        for room in self.world.rooms:
            glColor3ub(*room.color)
            glBegin(GL_TRIANGLE_FAN)
            for vert in room.verts:
                glVertex2f(*vert)
            glEnd()

        self.clockDisplay.draw()
