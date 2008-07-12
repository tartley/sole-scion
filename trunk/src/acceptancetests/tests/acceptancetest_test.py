import fix_pythonpath

from testutils.testcase import MyTestCase, run_test

class AcceptanceTest_test(MyTestCase):

    def testMe(self):
        self.fail("not tested")

if __name__ == "__main__":
    run_test()
