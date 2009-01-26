#!/usr/bin/python -O

import fixpath

from solescion.testutils.testcase import MyTestCase, run
from solescion.testutils.listener import Listener


class Listener_test(MyTestCase):

    def assert_is_reset(self, listener):
        self.assertFalse(listener.triggered, "not triggered")
        self.assertEquals(listener.triggerCount, 0, "0 triggercount")
        self.assertEquals(listener.args, None, "no args")
        self.assertEquals(listener.kwargs, None, "no kwargs")
        self.assertEquals(listener.args_list, [], "no args_list")
        self.assertEquals(listener.kwargs_list, [], "no kwargs_list")


    def test_constructor(self):
        listener = Listener()
        self.assert_is_reset(listener)


    def test_constructor_return_value(self):
        listener = Listener(return_value=456)
        self.assertEquals(listener.return_value, 456)


    def test_constructor_return_values(self):
        listener = Listener(return_values=[4, 5, 6])
        self.assertEquals(listener.return_values, [4, 5, 6])


    def test_call_no_args(self):
        listener = Listener()
        listener()
        self.assertTrue(listener.triggered, "no args triggered")
        self.assertEquals(listener.triggerCount, 1, "no args triggercount")
        self.assertEquals(listener.args, (), "no args args")
        self.assertEquals(listener.kwargs, {}, "no args kwargs")
        self.assertEquals(listener.args_list, [(),], "no args args_list")
        self.assertEquals(listener.kwargs_list, [{},], "no args kwargs_list")

        listener()
        self.assertTrue(listener.triggered, "no args triggered 2")
        self.assertEquals(listener.triggerCount, 2, "no args triggercount 2")
        self.assertEquals(listener.args, (), "no args args 2")
        self.assertEquals(listener.kwargs, {}, "no args kwargs 2")
        self.assertEquals(listener.args_list, [(),(),], "no args args_list 2")
        self.assertEquals(listener.kwargs_list, [{},{},],
            "no args kwargs_list 2")


    def test_call_with_args(self):
        listener = Listener()
        listener(1, 2, 3, a=7, b=8, c=9)
        self.assertTrue(listener.triggered, "with args triggered")
        self.assertEquals(listener.triggerCount, 1, "with args triggercount")
        self.assertEquals(listener.args, (1, 2, 3), "with args args")
        expKwargs1 = {'a':7, 'b':8, 'c':9}
        self.assertEquals(listener.kwargs, expKwargs1, "with args kwargs")
        self.assertEquals(listener.args_list, [(1, 2, 3),],
            "with args args_list")
        self.assertEquals(listener.kwargs_list, [expKwargs1,],
            "with args kwargs_list")

        listener(4, 5, 6, c=10, d=11, e=12)
        self.assertTrue(listener.triggered, "with args triggered 2")
        self.assertEquals(listener.triggerCount, 2, "with args triggercount 2")
        self.assertEquals(listener.args, (4, 5, 6), "with args args 2")
        expKwargs2 = {'c':10, 'd':11, 'e':12}
        self.assertEquals(listener.kwargs, expKwargs2, "with args kwargs 2")
        self.assertEquals(listener.args_list, [(1, 2, 3),(4, 5, 6),],
            "with args args_list 2")
        self.assertEquals(listener.kwargs_list, [expKwargs1, expKwargs2],
            "with args kwargs_list 2")


    def test_return_value(self):
        listener = Listener()
        self.assertNone(listener(), "default return value")
        listener.return_value = 456
        self.assertEquals(listener(), 456, "set return value 1")
        self.assertEquals(listener(), 456, "set return value 2")


    def test_return_values(self):
        listener = Listener()
        listener.return_values = [4, 3, 2]
        self.assertEquals(listener(), 4, "set return value list 1")
        self.assertEquals(listener(), 3, "set return value list 2")
        self.assertEquals(listener(), 2, "set return value list 3")
        self.assertEquals(listener(), None, "set return value list over 1")
        self.assertEquals(listener(), None, "set return value list over 2")


    def test_return_values_with_return_value(self):
        listener = Listener()
        listener.return_values = [4, 3, 2]
        listener.return_value = 456
        self.assertEquals(listener(), 4, "set return value list 1")
        self.assertEquals(listener(), 3, "set return value list 2")
        self.assertEquals(listener(), 2, "set return value list 3")
        self.assertEquals(listener(), 456, "set return value list over 1")
        self.assertEquals(listener(), 456, "set return value list over 2")


    def test_reset(self):
        listener = Listener()
        listener.return_values = [4, 3, 2]
        listener.return_value = 456
        listener(1, 2, 3, a=7, b=8, c=9)
        listener(4, 5, 6, c=10, d=11, e=12)
        listener.reset()
        self.assert_is_reset(listener)
        self.assertEquals(listener(), 2, "reset messed with return_values")
        self.assertEquals(listener(), 456, "reset messed with return_value")


    def test_call_preserves_args_identity(self):
        a = object()
        listener = Listener()
        listener(a)
        self.assertEquals(listener.args, (a,), "args should == a")


if __name__ == '__main__':
    run(Listener_test)

