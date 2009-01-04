from os.path import dirname, join
from distutils.core import setup
import py2exe
import pymunk

chipmunk_dll = join(dirname(pymunk.__file__), 'chipmunk.dll')

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

