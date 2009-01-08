#!/usr/bin/python -O

import fixpath

from pyglet.window import key

from solescion.testutils.listener import Listener
from solescion.testutils.testcase import MyTestCase, run

from solescion.controller.keyboard import Keyboard, on_key_press


class Keyboard_test(MyTestCase):

    def test_handlers(self):
        self.assertEquals(Keyboard.handlers, {},  "bad default handlers")

    def test_on_key_press(self):
        listener = Listener()
        Keyboard.handlers.update({key.SPACE: listener})
        on_key_press(key.ESCAPE, 0)
        self.assertFalse(listener.triggered, "should not trigger")
        on_key_press(key.SPACE, 0)
        self.assertTrue(listener.triggered, "should trigger")


if __name__=='__main__':
    run(Keyboard_test)

