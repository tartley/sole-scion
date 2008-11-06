import os
from distutils.core import setup
import py2exe

import pymunk

chipmunk_dll = os.path.join(os.path.dirname(pymunk.__file__), 'chipmunk.dll')

setup(
    windows=['run.py'],
    data_files=[
        ('.', [chipmunk_dll]),
    ],
    options={
        "py2exe":{
            "optimize": 2,
            "excludes": ['email', 'email.Utils'],
        }
    },
)

