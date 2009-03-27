#!/usr/bin/env python -O

import sys

from solescion.application import TITLE
from solescion.controller.gameloop import Gameloop


def main():

    if '-v' in sys.argv or '--version' in sys.argv:
        print TITLE
        import pymunk
        print 'pymunk:', pymunk.version
        import pyglet
        print 'pyglet:', pyglet.version
        sys.exit(0)

    gameloop = Gameloop()
    gameloop.init(TITLE)
    try:
        gameloop.run()
    finally:
        gameloop.dispose()


if __name__ == "__main__":
    main()

