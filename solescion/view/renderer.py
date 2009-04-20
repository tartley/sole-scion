from __future__ import division
from math import cos, sin, pi

from pyglet.gl import (
    glBegin, glClear, glClearColor, glColor3ub, glEnd, glPopMatrix,
    glPushMatrix, glTranslatef, glRotatef, glVertex2f,
    GL_COLOR_BUFFER_BIT, GL_TRIANGLE_FAN, GL_LINES,
)

from solescion.model.shards.block import Block
from solescion.model.shards.disc import Disc


class Renderer(object):
    "Draws OpenGL primitives to represent the current state of the model"
    # pylint: disable-msg=R0201
    #   Method could be a function: acknowledged.

    def __init__(self, camera):
        self.camera = camera


    def draw(self, world, aspect):
        "Draw the entire contents of the window"
        self.clear(world.material.color)
        self.camera.world_projection(aspect)
        self.draw_rooms(world.rooms)
        for chunk in world.chunks:
            self.draw_chunk(chunk)


    def clear(self, color):
        "Clear the window background with the given color"
        glClearColor(
            color[0] / 255,
            color[1] / 255,
            color[2] / 255,
            1.0)
        glClear(GL_COLOR_BUFFER_BIT)


    # TODO: not tested
    def draw_rooms(self, rooms):
        for room in rooms.itervalues():
            glColor3ub(*room.color)
            glBegin(GL_TRIANGLE_FAN)
            for vert in room.verts:
                glVertex2f(*vert)
            glEnd()
        for room in rooms.itervalues():
            glColor3ub(255, 255, 255)
            glBegin(GL_LINES)
            for idx in xrange(len(room.verts)):
                if idx not in room.neighbours:
                    glVertex2f(*room.verts[idx])
                    nextidx = (idx + 1) % len(room.verts)
                    glVertex2f(*room.verts[nextidx])
            glEnd()


    # TODO: not tested
    def draw_chunk(self, chunk):
        glPushMatrix()
        glTranslatef(chunk.body.position.x, chunk.body.position.y, 0)
        glRotatef(chunk.body.angle * 180 / pi, 0, 0, 1)

        for shard in chunk.shards:
            if type(shard) == Disc:
                self.draw_disc(shard)
            elif type(shard) == Block:
                self.draw_block(shard)
            else:
                raise TypeError("renderer cannot draw %s" % (type(chunk),))

        glPopMatrix()


    # TODO: not tested
    def draw_block(self, block):
        glBegin(GL_TRIANGLE_FAN)
        glColor3ub(
            int(block.material.color[0] * 0.25),
            int(block.material.color[1] * 0.25),
            int(block.material.color[2] * 0.25),
        )
        glVertex2f(0, 0)
        glColor3ub(*block.material.color)
        for idx in range(len(block.verts)):
            glVertex2f(*block.verts[idx])
        glVertex2f(*block.verts[0])
        glEnd()


    # TODO: not tested
    def draw_disc(self, disc):
        num_tris = 32
        x, y = disc.get_offset()
        glBegin(GL_TRIANGLE_FAN)
        darker = (
            int(disc.material.color[0] * 0.75),
            int(disc.material.color[1] * 0.75),
            int(disc.material.color[2] * 0.75),
        )
        glColor3ub(0, 0, 0)
        glVertex2f(x, y)
        col_freq = 4
        for idx in range(num_tris + 1):
            if idx % (col_freq * 2) == 0:
                glColor3ub(*disc.material.color)
            elif (idx + col_freq) % col_freq == 0:
                glColor3ub(*darker)
            theta = 2 * pi / num_tris * idx
            glVertex2f(
                x + disc.radius * sin(theta),
                y + disc.radius * cos(theta))
        glEnd()

