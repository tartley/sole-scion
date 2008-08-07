"Module of the 'Renderer' class"

from __future__ import division
from math import cos, sin, pi

from pyglet.gl import (
    glBegin, glClear, glClearColor, glColor3ub, glEnd, glPopMatrix,
    glPushMatrix, glTranslatef, glRotatef, glVertex2f,
    GL_COLOR_BUFFER_BIT, GL_TRIANGLE_FAN,
)

from model.shapes.block import Block
from model.shapes.disc import Disc


class Renderer(object):
    "Draws OpenGL primitives to represent the current state of the model"

    def __init__(self, camera):
        self.camera = camera


    def draw(self, world, aspect):
        "Draw the entire contents of the window"
        self.clear(world.backColor)
        self.camera.world_projection(aspect)
        for room in world.rooms:
            self.draw_room(room)
        for ent in world.entities:
            self.draw_entity(ent)


    def clear(self, color):
        "Clear the window background with the given color"
        glClearColor(
            color[0] / 255,
            color[1] / 255,
            color[2] / 255,
            1.0)
        glClear(GL_COLOR_BUFFER_BIT)


    def draw_room(self, room):
        "Draw the given room"
        glColor3ub(*room.color)
        glBegin(GL_TRIANGLE_FAN)
        for vert in room.verts:
            glVertex2f(*vert)
        glEnd()


    def draw_entity(self, ent):
        "Draw the given entity"
        glPushMatrix()
        glTranslatef(ent.x, ent.y, 0)
        glRotatef(ent.rot * 180 / pi, 0, 0, 1)

        if type(ent.shape) == Disc:
            self.draw_circle(ent)
        elif type(ent.shape) == Block:
            self.draw_poly(ent)
        else:
            raise TypeError("renderer cannot draw %s" % (type(ent),))

        glPopMatrix()


    def draw_poly(self, ent):
        "Draw the given polygonal entity"
        glColor3ub(255, 255, 0)
        glBegin(GL_TRIANGLE_FAN)
        for idx in range(len(ent.shape.verts)):
            glVertex2f(*ent.shape.verts[idx])
        glEnd()


    def draw_circle(self, ent):
        "Draw the given circular entity"
        numTris = 39
        glColor3ub(255, 255, 0)
        x, y = ent.shape.offset
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(x, y)
        for idx in range(numTris+1):
            theta = 2 * pi / numTris * idx
            glVertex2f(
                x + ent.shape.radius * sin(theta),
                y + ent.shape.radius * cos(theta))
        glEnd()


