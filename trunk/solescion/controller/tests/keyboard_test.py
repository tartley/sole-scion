#!/usr/bin/python -O

from pyglet.window import key

import fixpath

from testutils.listener import Listener
from testutils.testcase import MyTestCase, run_test

from controller.keyboard import handlers, on_key_press


class Keyboard_test(MyTestCase):

    def test_handlers(self):
        self.assertEquals(handlers, {},  "bad default handlers")

    def test_on_key_press(self):
        listener = Listener()
        handlers.update({key.SPACE: listener})
        on_key_press(key.ESCAPE, 0)
        self.assertFalse(listener.triggered, "should not trigger")
        on_key_press(key.SPACE, 0)
        self.assertTrue(listener.triggered, "should trigger")


if __name__=='__main__':
    run_test(Keyboard_test)

