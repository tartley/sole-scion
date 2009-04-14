from __future__ import division

from pyglet.window import key

from solescion.controller.keyboard import Keyboard
from solescion.model.chunk import Chunk
from solescion.model.material import steel
from solescion.model.shards.block import Block


def generate_ship():
    verts = [(-1, 0), (-2, 1), (0, 5), (2, 1), (1, 0)]
    return verts

MAX_TORQUE = 10000
SPIN_DRAG = 1500


class Player(object):

    def __init__(self):
        verts = generate_ship()
        block = Block(steel, verts)
        self.chunks = [Chunk(block)]


    def add_to_space(self, space, position, angle):
        self.chunks[0].add_to_space(space, (position[0]+1, position[1]), angle)


    def move(self):
        body = self.chunks[0].body
        if Keyboard.keystate[key.RIGHT]:
            torque = max(-MAX_TORQUE,
                min(0, -MAX_TORQUE - body.angular_velocity * SPIN_DRAG))
        elif Keyboard.keystate[key.LEFT]:
            torque = min(MAX_TORQUE,
                max(0, MAX_TORQUE - body.angular_velocity * SPIN_DRAG))
        else:
            torque = -body.angular_velocity * SPIN_DRAG
        body.torque = torque

        if Keyboard.keystate[key.UP]:
            body.apply_impulse(body.rotation_vector.rotated(90) * 150, (0, 0))
        elif Keyboard.keystate[key.DOWN]:
            body.apply_impulse(body.rotation_vector.rotated(-90) * 100, (0, 0))

