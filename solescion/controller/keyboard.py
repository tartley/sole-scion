# pylint: disable-msg=E0611
#   No name 'key' in module '_ModuleProxy'. No idea what this is.

from pyglet.window.key import KeyStateHandler, modifiers_string, symbol_string


keystate = KeyStateHandler()

handlers = {
}

def on_key_press(symbol, modifiers):
    if symbol in handlers:
        handlers[symbol]()

