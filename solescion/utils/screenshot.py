from os import fdopen, listdir
from os.path import expanduser, join
from tempfile import mkstemp

from PIL import Image

from pyglet.image import get_buffer_manager

from setup import NAME


def _get_filename(prefix, extension):
    homedir = expanduser("~")
    existing = listdir(homedir)
    for idx in range(100):
        candidate = "%s%02d%s" % (prefix, idx, extension)
        if candidate not in existing:
            return join(homedir, candidate)
    return None


def _create_tempfile():
    "Caller's responsibility to close and/or delete the file after use"
    filedesc, fname = mkstemp(prefix='testimage-', suffix='.png')
    tempfile = fdopen(filedesc, "w+b")
    return tempfile, fname


def image_from_window(window):
    "Convert given Pyglet Window into a PIL Image"
    tempfile, fname = _create_tempfile()
    window.switch_to()
    get_buffer_manager().get_color_buffer().save(filename=fname, file=tempfile)
    tempfile.seek(0)
    image = Image.open(tempfile)
    return image


def save_screenshot(window):
    filename = _get_filename("%s-screenshot-" % NAME, ".png")
    if filename:
        image = image_from_window(window)
        image.save(filename)
        print "Saved screenshot at %s" % (filename)

