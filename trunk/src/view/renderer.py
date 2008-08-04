"""
Draws OpenGL primitives to represent the current state of the model
"""
from __future__ import division

from pyglet import clock
from pyglet.gl import (
    glBegin, glClear, glClearColor, glColor3ub, glEnd, glVertex2f,
    GL_COLOR_BUFFER_BIT, GL_TRIANGLE_FAN,
)


class Renderer(object):
    """Sole class of the renderer module"""

    def __init__(self, camera):
        self.camera = camera
        self.clockDisplay = clock.ClockDisplay()


    def draw(self, world, aspect):
        """Draw everything that is visible in the window"""
        self.clear(world.backColor)
        self.camera.world_projection(aspect)
        self.draw_world(world)


    def clear(self, color):
        """Clear the window background with the given color"""
        glClearColor(
            color[0] / 255,
            color[1] / 255,
            color[2] / 255,
            1.0)
        glClear(GL_COLOR_BUFFER_BIT)


    def draw_world(self, world):
        """Draw the given world in its entirety"""
        for room in world.rooms:
            glColor3ub(*room.color)
            glBegin(GL_TRIANGLE_FAN)
            for vert in room.verts:
                glVertex2f(*vert)
            glEnd()


