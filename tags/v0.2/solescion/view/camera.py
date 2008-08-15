"""
Camera tracks a position, orientation and zoom level, and applies openGL
transforms so that subsequent renders are drawn at the correct place, size
and orientation on screen
"""

from __future__ import division
from math import sin, cos

from pyglet.gl import (
    glLoadIdentity, glMatrixMode,
    gluLookAt, gluOrtho2D,
    GL_MODELVIEW, GL_PROJECTION,
)


class Camera(object):

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.scale = 1.0
        self.rot = 0.0


    def world_projection(self, aspect):
        """Sets OpenGL projection and modelview matrices such that the window
        is centered on self.(x,y), shows at least scale world units in every
        direction, and is oriented by rot."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
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

