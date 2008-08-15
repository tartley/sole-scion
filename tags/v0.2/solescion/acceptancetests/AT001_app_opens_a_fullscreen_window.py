#!/usr/bin/python -O
from __future__ import division
from unittest import TestCase

import fixpath

from acceptancetest import AcceptanceTest
from testutils.testcase import run_test

from run import main


class AT001_app_opens_a_fullscreen_window(AcceptanceTest):

    def is_window_visible(self):
        win = self.get_window()
        return win and win.visible


    def is_window_fullscreen(self):
        win = self.get_window()
        return win and win.fullscreen


    def test_window(self):
        conditions = [
            self.is_window_visible,
            self.is_window_fullscreen,
        ]
        self.set_conditions(conditions)
        main()


if __name__ == "__main__":
    run_test(AT001_app_opens_a_fullscreen_window)

