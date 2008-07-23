#!/usr/bin/python -O

import fixpath

from testutils.testcase import MyTestCase, run_test

from testutils.listener import Listener


class Listener_test(MyTestCase):

    def assert_is_reset(self, listener):
        self.assertFalse(listener.triggered, "not triggered")
        self.assertEquals(listener.triggerCount, 0, "0 triggercount")
        self.assertEquals(listener.args, None, "no args")
        self.assertEquals(listener.kwargs, None, "no kwargs")
        self.assertEquals(listener.argsList, [], "no argslist")
        self.assertEquals(listener.kwargsList, [], "no kwargslist")


    def testConstructor(self):
        listener = Listener()
        self.assert_is_reset(listener)


    def testCall_no_args(self):
        listener = Listener()
        listener()
        self.assertTrue(listener.triggered, "no args triggered")
        self.assertEquals(listener.triggerCount, 1, "no args triggercount")
        self.assertEquals(listener.args, (), "no args args")
        self.assertEquals(listener.kwargs, {}, "no args kwargs")
        self.assertEquals(listener.argsList, [(),], "no args argslist")
        self.assertEquals(listener.kwargsList, [{},], "no args kwargslist")

        listener()
        self.assertTrue(listener.triggered, "no args triggered 2")
        self.assertEquals(listener.triggerCount, 2, "no args triggercount 2")
        self.assertEquals(listener.args, (), "no args args 2")
        self.assertEquals(listener.kwargs, {}, "no args kwargs 2")
        self.assertEquals(listener.argsList, [(),(),], "no args argslist 2")
        self.assertEquals(listener.kwargsList, [{},{},],
            "no args kwargslist 2")


    def testCall_with_args(self):
        listener = Listener()
        listener(1, 2, 3, a=7, b=8, c=9)
        self.assertTrue(listener.triggered, "with args triggered")
        self.assertEquals(listener.triggerCount, 1, "with args triggercount")
        self.assertEquals(listener.args, (1, 2, 3), "with args args")
        expKwargs1 = {'a':7, 'b':8, 'c':9}
        self.assertEquals(listener.kwargs, expKwargs1, "with args kwargs")
        self.assertEquals(listener.argsList, [(1, 2, 3),], "with args argslist")
        self.assertEquals(listener.kwargsList, [expKwargs1,],
            "with args kwargslist")

        listener(4, 5, 6, c=10, d=11, e=12)
        self.assertTrue(listener.triggered, "with args triggered 2")
        self.assertEquals(listener.triggerCount, 2, "with args triggercount 2")
        self.assertEquals(listener.args, (4, 5, 6), "with args args 2")
        expKwargs2 = {'c':10, 'd':11, 'e':12}
        self.assertEquals(listener.kwargs, expKwargs2, "with args kwargs 2")
        self.assertEquals(listener.argsList, [(1, 2, 3),(4, 5, 6),],
            "with args argslist 2")
        self.assertEquals(listener.kwargsList, [expKwargs1, expKwargs2],
            "with args kwargslist 2")


    def testReturn_value(self):
        listener = Listener()
        self.assertNone(listener(), "default return value")
        listener.returnValue = 456
        self.assertEquals(listener(), 456, "set return value 1")
        self.assertEquals(listener(), 456, "set return value 2")


    def testReturnValueList(self):
        listener = Listener()
        listener.returnValueList = [4, 3, 2]
        self.assertEquals(listener(), 4, "set return value list 1")
        self.assertEquals(listener(), 3, "set return value list 2")
        self.assertEquals(listener(), 2, "set return value list 3")
        self.assertEquals(listener(), None, "set return value list over 1")
        self.assertEquals(listener(), None, "set return value list over 2")


    def testReturnValueList_with_returnValue(self):
        listener = Listener()
        listener.returnValueList = [4, 3, 2]
        listener.returnValue = 456
        self.assertEquals(listener(), 4, "set return value list 1")
        self.assertEquals(listener(), 3, "set return value list 2")
        self.assertEquals(listener(), 2, "set return value list 3")
        self.assertEquals(listener(), 456, "set return value list over 1")
        self.assertEquals(listener(), 456, "set return value list over 2")


    def testReset(self):
        listener = Listener()
        listener.returnValueList = [4, 3, 2]
        listener.returnValue = 456
        listener(1, 2, 3, a=7, b=8, c=9)
        listener(4, 5, 6, c=10, d=11, e=12)
        listener.reset()
        self.assert_is_reset(listener)
        self.assertEquals(listener(), 2, "reset messed with returnValueList")
        self.assertEquals(listener(), 456, "reset messed with returnValue")


    def testCall_deep_clones_args(self):
        a = [2, 3, 4]
        b = [11, a, 55]
        listener = Listener()
        listener(b)
        a.append('xxx')
        expected = ([11, [2, 3, 4], 55],)
        self.assertEquals(listener.args, expected, "should clone args")


if __name__ == '__main__':
    run_test()

