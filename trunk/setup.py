from distutils.core import setup
from sys import argv

if 'py2exe' in argv:

    import py2exe

    args = dict(
        windows=['run.py'],
        options={
            "py2exe":{
                "optimize": 2,
                "excludes": ['email', 'email.Utils'],
            }
        },
        data_files = [
            ('', ['pymunk/chipmunk.dll']),
        ],
    )

else:

    args = dict(
        name = 'solescion',
        version = '0.2.2dev',
        url = 'http://code.google.com/p/sole-scion/',
        author = 'Jonathan Hartley',
        author_email = 'tartley@tartley.com',
        description = 'A game with 2D vector graphics and rigid-body physics.',

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

setup(**args)

