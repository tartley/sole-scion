#!/usr/bin/python -O

import fixpath

from solescion.testutils.testcase import MyTestCase, run

class AcceptanceTest_test(MyTestCase):

    def testMe(self):
        pass

if __name__ == "__main__":
    run(AcceptanceTest_test)
