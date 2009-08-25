from __future__ import with_statement
from os import listdir, mkdir
from os.path import isdir, join
from sys import argv
from shutil import copy, move, rmtree
from zipfile import ZipFile

from setuptools import setup, find_packages

from solescion import name, version

WIN_BINARY = '%s-win-binary-%s' % (name, version)
EXE_DIR = 'exe'


def py2exe():

    import py2exe

    setup(
        windows=['run.py'],
        options={
            'py2exe':{
                'dist_dir': join('dist', WIN_BINARY, EXE_DIR),
                'excludes': [
                    'email',
                    'email.Utils',
                    'Tkinter',
                ],
                'optimize': 2,
            }
        },
        data_files = [
            ('', ['pymunk/chipmunk.dll']),
        ],
    )


def other():

    setup(
        name = name,
        version = version,
        url = 'http://code.google.com/p/sole-scion/',
        author = 'Jonathan Hartley',
        author_email = 'tartley@tartley.com',
        description =
            'A game with 2D vector graphics and rigid body physics.',

        py_modules = [
            'run',
            'run_tests',
        ],
        packages = [
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


def create_batch_file():
    batch_file = join('dist', WIN_BINARY, '%s.bat' % (name,))
    with open(batch_file, 'w') as f:
        f.write('@echo off\n%s\\run.exe\n' % EXE_DIR)


def zip_directory():
    def zip_dir(archive, prefix, path):
        '''
        archive=zip file to write to
        prefix+path=directory to be zipped
        prefix is stripped from the paths within the zip
        '''
        fullpath = join(prefix, path)
        for filename in listdir(fullpath):
            filepath = join(fullpath, filename)
            zippath = join(path, filename)
            if isdir(filepath):
                zip_dir(archive, prefix, zippath)
            else:
                archive.write(filepath, zippath)

    zipname = join('dist', '%s.zip' % (WIN_BINARY,))
    archive = ZipFile(zipname, 'w')
    zip_dir(archive, 'dist', WIN_BINARY)
    archive.close()


def main():
    if 'py2exe' in argv:
        py2exe()
        create_batch_file()
        zip_directory()
    else:
        other()

if __name__ == '__main__':
    main()


