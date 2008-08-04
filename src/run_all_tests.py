#!/usr/bin/python -O
"Runs all unit and acceptance tests"

from unittest import TextTestRunner

from testutils.testcase import combine

from acceptancetests.tests.acceptancetest_test import AcceptanceTest_test
from controller.tests.gameloop_test import Gameloop_test
from model.tests.entity_test import Entity_test
from model.tests.room_test import Room_test
from model.tests.world_test import World_test
from testutils.tests.testimage_test import TestImage_test
from testutils.tests.listener_test import Listener_test
from testutils.tests.testcase_test import TestCase_test
from view.tests.camera_test import Camera_test

from acceptancetests.AT001_app_opens_a_fullscreen_window import \
    AT001_app_opens_a_fullscreen_window


def run_all_tests():
    "Runs all unit and acceptance tests"
    runner = TextTestRunner(verbosity=2)
    suite = combine(
        AcceptanceTest_test,
        Gameloop_test,
        Entity_test,
        Room_test,
        World_test,
        TestImage_test,
        Listener_test,
        TestCase_test,
        Camera_test,
        AT001_app_opens_a_fullscreen_window,
    )
    runner.run(suite)



if __name__ == "__main__":
    run_all_tests()
