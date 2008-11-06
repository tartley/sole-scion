#!/usr/bin/env python -O

from sys import argv, exit, path

from solescion.application import title
from solescion.controller.gameloop import Gameloop


def main():

    if '-v' in argv or '--version' in argv:
        print title
        import pymunk
        print 'pymunk:', pymunk.version
        import pyglet
        print 'pyglet:', pyglet.version
        exit(0)

    gameloop = Gameloop()
    gameloop.init(title)
    try:
        gameloop.run()
    finally:
        gameloop.dispose()


if __name__ == "__main__":
    main()

