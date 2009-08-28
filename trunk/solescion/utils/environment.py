
from os import environ

def append(var, value):
    values = environ.get(var, '')
    if value:
        value += ';'
    value += 'shapely'
    environ[var] = value

def add_lib_to_path():
    'required for shapely to find its own DLL files'

    append('PATH', 'solescion\\lib') # for mswin source
    # append('LD_LIBRARY_PATH', 'solescion\\lib') # for linux

