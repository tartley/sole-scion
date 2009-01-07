#!/usr/bin/python -O
"Run all unit and acceptance tests"

from solescion.testutils.testcase import combine, run_test

from solescion.acceptancetests.tests.acceptancetest_test import AcceptanceTest_test
from solescion.controller.tests.gameloop_test import Gameloop_test
from solescion.model.tests.chunk_test import Chunk_test
from solescion.model.tests.room_test import Room_test
from solescion.model.tests.world_test import World_test
from solescion.model.tests.material_test import Material_test
from solescion.model.shards.tests.disc_test import Disc_test
from solescion.model.shards.tests.block_test import Block_test
from solescion.testutils.tests.testimage_test import TestImage_test
from solescion.testutils.tests.listener_test import Listener_test
from solescion.testutils.tests.testcase_test import TestCase_test
from solescion.view.tests.camera_test import Camera_test
from solescion.view.tests.renderer_test import Renderer_test

from solescion.acceptancetests.AT001_app_opens_a_fullscreen_window import \
    AT001_app_opens_a_fullscreen_window


def run_all_tests():
    suite = combine(
        AcceptanceTest_test,
        Gameloop_test,
        Chunk_test,
        Room_test,
        World_test,
        Material_test,
        Disc_test,
        Block_test,
        TestImage_test,
        Listener_test,
        TestCase_test,
        Camera_test,
        Renderer_test,
        AT001_app_opens_a_fullscreen_window,
    )
    run_test(suite)


if __name__ == "__main__":
    run_all_tests()

