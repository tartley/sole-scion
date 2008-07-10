#!/usr/bin/python -O
from unittest import TextTestRunner

from testutils.testcase import combine

from acceptancetests.tests.acceptancetest_test import AcceptanceTest_test
from controller.tests.gameloop_test import Gameloop_test
from model.tests.world_test import World_test
from testutils.tests.testcase_test import TestCase_test
from view.tests.renderer_test import Renderer_test

from acceptance_tests.AT001_app_opens_a_fullscreen_window import \
    AT001_app_opens_a_fullscreen_window


def run_all_tests():
    runner = TextTestRunner(verbosity=2)
    suite = combine(
        AcceptanceTest_test,
        TestCase_test,
        Gameloop_test,
        Renderer_test,
        AT001_app_opens_a_fullscreen_window,
    )
    runner.run(suite)


if __name__ == "__main__":
    run_all_tests()
