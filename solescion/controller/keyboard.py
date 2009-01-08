# pylint: disable-msg=E0611
#   No name 'key' in module '_ModuleProxy'. No idea what this is.

from pyglet.window.key import KeyStateHandler


class Keyboard(object):
    keystate = KeyStateHandler()
    handlers = {}


def on_key_press(symbol, _):
    if symbol in Keyboard.handlers:
        Keyboard.handlers[symbol]()

