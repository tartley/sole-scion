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

    # TODO: remove window. We only need aspect of width/height
    def __init__(self, world, window):
        self.world = world
        self.window = window
        self.scale = 1.0
        self.x = 0.0
        self.y = 0.0
        self.rot = 0.0
        self.world_projection()

        # TODO: where should this live?
        self.clockDisplay = clock.ClockDisplay()


    def clear(self, color):
        glClearColor(
            color[0] / 255,
            color[1] / 255,
            color[2] / 255,
            1.0)
        glClear(GL_COLOR_BUFFER_BIT)


    def world_projection(self):
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


    def draw_rooms(self):
        for room in self.world.rooms:
            glColor3ub(*room.color)
            glBegin(GL_TRIANGLE_FAN)
            for vert in room.verts:
                glVertex2f(*vert)
            glEnd()

    def hud_projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # TODO: some glu command. copy from gameloop3_flowers


    def draw_hud(self):
        self.clockDisplay.draw()


    def draw(self):
        self.clear(self.world.backColor)
        self.world_projection()
        self.draw_rooms()
        self.hud_projection()
        self.draw_hud()

