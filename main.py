#!/usr/bin/env python -O

from os import environ

def append_environ(var, value):
    values = environ.get(var, '')
    if value:
        value += ';'
    value += 'shapely'
    environ[var] = value

# required for shapely to find its own .dll files
append_environ('PATH', 'shapely') # for mswin
append_environ('LD_LIBRARY_PATH', 'shapely') # for linux

from solescion.controller.application import main

if __name__ == "__main__":
    main()

