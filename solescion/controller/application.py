from os import curdir
from os.path import abspath, dirname
import sys

from solescion import name, version
from solescion.controller.gameloop import Gameloop


def relpath(path):
    path = dirname(path)
    abs_cwd = abspath(curdir)
    if path.startswith(abs_cwd):
        path = '.' + path[len(abs_cwd):]
    return path


class Application(object):

    def __init__(self):
        self.gameloop = None
        self.profile = False


    def parse_args(self, args):
        if '-v' in sys.argv or '--version' in sys.argv:
            self.print_version_info()
            sys.exit(0)
        if '-p' in sys.argv or '--profile' in sys.argv:
            self.profile = True


    def print_version_info(self):
        print name, version
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


    def run_gameloop(self):
        if self.profile:
            import cProfile
            command = 'gameloop.run()'
            cProfile.runctx(
                command, globals(), locals(), filename='profile.out')
        else:
            self.gameloop.run()


    def run(self):
        self.parse_args(sys.argv)
        self.gameloop = Gameloop()
        self.gameloop.init(name, version)
        try:
            self.run_gameloop()
        finally:
            self.gameloop.dispose()


def main():
    app = Application()
    app.run()


