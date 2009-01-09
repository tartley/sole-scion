from distutils.core import setup
from os.path import dirname, join
import platform

import pymunk

is_windows = platform.system() in ['Microsoft', 'Windows']
if is_windows:
    import py2exe


def getargs():

    args = dict(
        name='solescion',
        version='0.2.2dev',
        url='http://code.google.com/p/sole-scion/',
        author='Jonathan Hartley',
        author_email='tartley@tartley.com',

        py_modules = ['run', 'run_tests'],
        packages = [
            'pyglet',
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
    win_args = dict(
        windows=['run.py'],
        options={
            "py2exe":{
                "optimize": 2,
                "excludes": ['email', 'email.Utils'],
            }
        },
        data_files=[
            ('.', [join(dirname(pymunk.__file__), 'chipmunk.dll')]),
        ],
    )

    if is_windows:
        args.update(win_args)

    return args


setup(**getargs())

