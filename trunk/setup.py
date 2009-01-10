from __future__ import with_statement
from distutils.core import setup
from os import mkdir
from os.path import join
from sys import argv
from shutil import copy, move, rmtree


NAME = 'SoleScion'
VERSION = '0.2.2dev'
WIN_BINARY = '%s-win-binary-%s' % (NAME, VERSION)
EXE_DIR = 'exe'

def py2exe():

    import py2exe

    setup(
        windows=['run.py'],
        options={
            'py2exe':{
                'dist_dir': join('dist', WIN_BINARY, EXE_DIR),
                'excludes': [
                    'email',
                    'email.Utils',
                    'Tkinter',
                ],
                'optimize': 2,
            }
        },
        data_files = [
            ('', ['pymunk/chipmunk.dll']),
        ],
    )


def other():

    setup(
        name = NAME,
        version = VERSION,
        url = 'http://code.google.com/p/sole-scion/',
        author = 'Jonathan Hartley',
        author_email = 'tartley@tartley.com',
        description = 'A game with 2D vector graphics and rigid body physics.',

        py_modules = [
            'run',
            'run_tests',
        ],
        packages = [
            'pyglet',
            'pyglet.app',
            'pyglet.font',
            'pyglet.gl',
            'pyglet.graphics',
            'pyglet.image',
            'pyglet.image.codecs',
            'pyglet.text',
            'pyglet.text.formats',
            'pyglet.window',
            'pyglet.window.carbon',
            'pyglet.window.win32',
            'pyglet.window.xlib',
            'pymunk',
            'solescion',
            'solescion.acceptancetests',
            'solescion.acceptancetests.tests',
            'solescion.controller',
            'solescion.controller.tests',
            'solescion.model',
            'solescion.model.tests',
            'solescion.model.shards',
            'solescion.model.shards.tests',
            'solescion.testutils',
            'solescion.testutils.tests',
            'solescion.utils',
            'solescion.utils.tests',
            'solescion.view',
            'solescion.view.tests',
        ],
    )


def create_win_binary_batch_file():
    batch_file = join('dist', WIN_BINARY, '%s.bat' % (NAME,))
    with open(batch_file, 'w') as f:
        f.write('@echo off\n%s\\run.exe\n' % EXE_DIR)


def main():
    if 'py2exe' in argv:
        py2exe()
        create_win_binary_batch_file()
    else:
        other()

if __name__ == '__main__':
    main()


