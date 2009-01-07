from sys import path
from os.path import abspath, dirname

depth = 3
absdir = abspath(dirname(__file__) + '/..' * depth)
path.insert(0, absdir)

