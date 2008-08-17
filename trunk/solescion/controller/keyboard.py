from pyglet.window import key

handlers = {
}

def on_key_press(symbol, modifiers):
    if symbol in handlers:
        handlers[symbol]()
