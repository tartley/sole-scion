import sys
from os.path import abspath, dirname

depth = 4
absdir = abspath(dirname(__file__) + '/..' * depth)
sys.path.insert(0, absdir)

