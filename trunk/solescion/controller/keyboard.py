# pylint: disable-msg=E0611
#   No name 'key' in module '_ModuleProxy'. No idea what this is.

from pyglet.window.key import modifiers_string, symbol_string

handlers = {
}

def on_key_press(symbol, modifiers):
    if symbol in handlers:
        handlers[symbol]()
    else:
        print "key:", symbol_string(symbol), modifiers_string(modifiers)
