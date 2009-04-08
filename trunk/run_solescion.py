#!/usr/bin/env python -O

import sys

from solescion.application import TITLE
from solescion.controller.gameloop import Gameloop


def main():

    profile = False
    if '-v' in sys.argv or '--version' in sys.argv:
        print TITLE
        import pymunk
        print 'pymunk:', pymunk.version
        import pyglet
        print 'pyglet:', pyglet.version
        sys.exit(0)
    if '-p' in sys.argv or '--profile' in sys.argv:
        profile = True

    gameloop = Gameloop()
    gameloop.init(TITLE)
    try:
        if profile:
            import cProfile
            command = 'gameloop.run()'
            cProfile.runctx(
                command, globals(), locals(), filename='profile.out')
        else:
            gameloop.run()
    finally:
        gameloop.dispose()


if __name__ == "__main__":
    main()

