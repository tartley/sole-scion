#!/usr/bin/env python -O

from os import curdir
from os.path import abspath, dirname
import sys

from solescion.application import TITLE
from solescion.controller.gameloop import Gameloop

def relpath(path):
    path = dirname(path)
    abs_cwd = abspath(curdir)
    if path.startswith(abs_cwd):
        path = '.' + path[len(abs_cwd):]
    return path


def main():

    profile = False
    if '-v' in sys.argv or '--version' in sys.argv:
        import platform
        import pymunk
        import pyglet
        import shapely
        from shapely import geos
        print TITLE
        print 'pymunk:', pymunk.version, relpath(pymunk.__file__)
        print 'pyglet:', pyglet.version, relpath(pyglet.__file__)
        print 'shapely:', geos.lgeos.GEOSversion(), relpath(shapely.__file__)
        print 'python:', platform.python_version()
        print 'platform:', platform.machine(), platform.platform()
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

