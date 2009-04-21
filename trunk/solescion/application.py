from os import curdir
from os.path import abspath, dirname
import sys

from solescion.controller.gameloop import Gameloop


NAME = 'SoleScion'
VERSION = '0.2.5-svn'


def relpath(path):
    path = dirname(path)
    abs_cwd = abspath(curdir)
    if path.startswith(abs_cwd):
        path = '.' + path[len(abs_cwd):]
    return path

def print_version_info():
    print NAME, VERSION
    import platform
    print 'Python %s, %s' % (platform.python_version(), platform.platform())
    import pyglet
    print 'pyglet %s, %s' % (pyglet.version, relpath(pyglet.__file__))
    import pymunk
    print 'Pymunk %s, %s' % (pymunk.version, relpath(pymunk.__file__))
    import shapely
    from shapely import geos
    print 'Shapely %s, %s' % (
        geos.lgeos.GEOSversion(), relpath(shapely.__file__))


def main():

    profile = False
    if '-v' in sys.argv or '--version' in sys.argv:
        print_version_info()
        sys.exit(0)
    if '-p' in sys.argv or '--profile' in sys.argv:
        profile = True

    gameloop = Gameloop()
    gameloop.init(NAME, VERSION)
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


