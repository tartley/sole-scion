from __future__ import division

from pyglet.window import key

from solescion.controller.keyboard import Keyboard
from solescion.model.chunk import Chunk
from solescion.model.material import Material
from solescion.model.shards.block import Block


def generate_ship():
    verts = [(-1, 0), (-2, 1), (0, 5), (2, 1), (1, 0)]
    return verts


class Player(object):

    def __init__(self):
        verts = generate_ship()
        block = Block(Material.steel, verts)
        self.chunks = [Chunk(block)]


    def add_to_space(self, space, position, angle):
        self.chunks[0].add_to_space(space, (position[0]+1, position[1]), angle)


    def move(self):
        body = self.chunks[0].body
        if Keyboard.keystate[key.RIGHT]:
            torque = -3000
        elif Keyboard.keystate[key.LEFT]:
            torque = +3000
        else:
            torque = -body.angular_velocity * 1000
        body.torque = torque

        if Keyboard.keystate[key.UP]:
            body.apply_impulse(body.rotation_vector.rotated(90) * 150, (0, 0))
        elif Keyboard.keystate[key.DOWN]:
            body.apply_impulse(body.rotation_vector.rotated(-90) * 100, (0, 0))

