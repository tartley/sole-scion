from os import fdopen, listdir
from os.path import expanduser, join
from tempfile import mkstemp

from pyglet.image import get_buffer_manager

from setup import NAME


def _get_filename(prefix, extension):
    homedir = expanduser("~")
    existing = listdir(homedir)
    for idx in range(100):
        candidate = "%s%03d%s" % (prefix, idx, extension)
        if candidate not in existing:
            return join(homedir, candidate)
    return None


def _create_tempfile():
    "Caller's responsibility to close and/or delete the file after use"
    filedesc, fname = mkstemp(prefix='testimage-', suffix='.png')
    tempfile = fdopen(filedesc, "w+b")
    return tempfile, fname


def save_screenshot(window):
    filename = _get_filename("%s-screenshot-" % NAME, ".png")
    if filename:
        image = get_buffer_manager().get_color_buffer()
        image.save(filename)

