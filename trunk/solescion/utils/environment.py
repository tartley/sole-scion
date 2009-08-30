
from os import environ
from os.path import join
from platform import system


if system() == 'Windows':
    separator = ';'
    var_name = 'PATH'
else:
    separator = ':'
    var_name = 'LD_LIBRARY_PATH'


def append(name, suffix):
    print 'append', name, suffix
    value = environ.get(name, '')
    print 'orig', value
    if value:
        value += separator
    value += suffix
    environ[name] = value
    print 'set', name, '=', value


def add_lib_to_path():
    append(var_name, join('solescion', 'lib'))

