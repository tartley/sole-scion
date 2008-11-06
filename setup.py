from distutils.core import setup
import py2exe

setup(
    windows=['run.py'],
    options={
        "py2exe":{
            "optimize": 2,
            "excludes": ['email', 'email.Utils'],
        }
    }
)

