#!/usr/bin/python -O
from __future__ import division

# pylint: disable-msg=W0611
#   unused import: acknowledged
import fixpath

from solescion.acceptancetests.acceptancetest import AcceptanceTest, get_window
from solescion.testutils.testcase import run

from solescion.controller.application import main


def is_window_visible():
    print 'is_visible'
    win = get_window()
    return win and win.visible


def is_window_fullscreen():
    print 'is_fullscreen'
    win = get_window()
    return win and win.fullscreen


class AT001(AcceptanceTest):
    # pylint: disable-msg=R0904
    #   Too many public methods: we are a subclass of unittest.TestCase

    def test_window(self):
        conditions = [
            is_window_visible,
            is_window_fullscreen,
        ]
        self.set_conditions(conditions)
        main()


if __name__ == "__main__":
    run(AT001)

