#!/usr/bin/python -O
from unittest import (
    main, TestLoader, TestCase as RealTestCase, TestSuite, TextTestRunner)
from ctypes import Array

import fixpath

from pyglet.gl import GLint
from pymunk import Vec2d

from solescion.testutils.listener import Listener
from solescion.testutils.testcase import (
    _compare_indexables, _compare_lengths, _compare_types, _is_int_indexable,
    _tostr,
    combine, MyTestCase, run,
)


class TestCase_module_functions_test(MyTestCase):

    def test_is_int_indexable(self):
        self.assertTrue(_is_int_indexable([]), "list")
        self.assertTrue(_is_int_indexable(()), "tuple")
        self.assertTrue(_is_int_indexable((GLint * 1)(*[1])), "Array1")
        self.assertTrue(_is_int_indexable('a'), "str")

        # TODO: probably dicts and sets should pretty output too
        self.assertFalse(_is_int_indexable({}), "dict")
        self.assertFalse(_is_int_indexable(set()), "set")
        self.assertFalse(_is_int_indexable(1), "int")
        self.assertFalse(_is_int_indexable(1.1), "float")


    def test_tostr(self):
        items = [
            1, 1.2, 'abc',
            [1, 2, 3], (1, 2, 3), set([1, 2, 3]),
            {'a':1, 'b':2, 'c':3},
        ]
        for i in items:
            self.assertEquals(_tostr(i), str(i),
                'tostr() for %s' % str(type(i)))

        array = (GLint * 3)(1, 2, 3)
        self.assertEquals(_tostr(array), "Array(1, 2, 3)", "Array")


    def test_compare_lengths(self):
        _compare_lengths((1, 2, 3), [1, 2, 3], None)
        self.assertRaises(
            lambda: _compare_lengths((1, 2, 3), [1, 2, 3, 4], None),
            AssertionError)
        self.assertRaises(
            lambda: _compare_lengths((1, 2, 3), [1, 2], None),
            AssertionError)


    def test_compare_indexables(self):
        _compare_indexables((1, 2, 3), [1, 2, 3], None)
        self.assertRaises(
            lambda: _compare_indexables((1, 2, 3), [1, 2, 4], None),
            AssertionError)
        self.assertRaises(
            lambda: _compare_indexables((1, 2, 3), [1, 2, 3, 4], None),
            AssertionError)
        self.assertRaises(
            lambda: _compare_indexables((1, 2, 3, 4), [1, 2, 3], None),
            AssertionError)


    def test_compare_types(self):
        _compare_types(0, 1, None)
        self.assertRaises(lambda: _compare_types(0, 0.1, None), AssertionError)

        array3 = (GLint * 3)(1, 2, 3)
        array4 = (GLint * 4)(1, 2, 3, 4)
        _compare_types(array3, array4, None)


class ClassUnderTest(MyTestCase):

    def testAlwaysPasses(self):
        pass


class TestCase_assertEquals_test(RealTestCase):

    def setUp(self):
        self.mytestcase = ClassUnderTest("testAlwaysPasses")


    def testAssertNone(self):
        self.mytestcase.assertNone(None)
        self.mytestcase.assertNone(None, 'msg')

        assertion = lambda: self.mytestcase.assertNone(0)
        expectedMsg = "not None: 0\n  "
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)

        assertion = lambda: self.mytestcase.assertNone(0, 'msg')
        expectedMsg = "not None: 0\n  msg"
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)


    def testAssertNotNone(self):
        self.mytestcase.assertNotNone(0)
        self.mytestcase.assertNotNone(0, 'msg')

        assertion = lambda: self.mytestcase.assertNotNone(None)
        expectedMsg = "is None\n  "
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)

        assertion = lambda: self.mytestcase.assertNotNone(None, 'msg')
        expectedMsg = "is None\n  msg"
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)


    def testAssertEquals_shows_values_in_exception_message(self):
        assertion = lambda: self.mytestcase.assertEquals(2, 3, "desc")
        expectedMsg = "2 != 3\n  desc"
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)


    def testAssertEquals_types_differ(self):
        assertion = lambda: self.mytestcase.assertEquals((1, 2, 3), [1, 2, 3])
        expectedMsg = (
            "not equal. types differ:\n"
            "  <type 'tuple'> (1, 2, 3)\n"
            "  <type 'list'> [1, 2, 3]\n")
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)

        assertion = lambda: self.mytestcase.assertEquals(
            (1, 2, 3), [1, 2, 3], "message")
        expectedMsg += "message"
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)


    def testAssertEquals_iterables_of_different_lengths(self):
        assertion = lambda: self.mytestcase.assertEquals(
            [1, 2, 3], [1, 2, 3, 4])
        expectedMsg = (
            "not equal, lengths differ: 3 != 4\n"
            "  [1, 2, 3]\n"
            "  [1, 2, 3, 4]\n")
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)


    def testAssertEquals_ctypes_arrays_same(self):
        one = (GLint * 4)(*[1, 2, 3, 4])
        same = (GLint * 4)(*[1, 2, 3, 4])
        self.mytestcase.assertEquals(one, same, "similar arrays should pass")


    def testAssertEquals_ctypes_arrays_shorter(self):
        one = (GLint * 4)(*[1, 2, 3, 4])
        shorter = (GLint * 3)(*[1, 2, 3])
        assertion = lambda: self.mytestcase.assertEquals(one, shorter)
        expectedMsg = (
            "not equal, lengths differ: 4 != 3\n"
            "  Array(1, 2, 3, 4)\n"
            "  Array(1, 2, 3)\n")
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)


    def testAssertEquals_ctypes_arrays_longer(self):
        one = (GLint * 4)(*[1, 2, 3, 4])
        longer = (GLint * 5)(*[1, 2, 3, 4, 5])
        assertion = lambda: self.mytestcase.assertEquals(one, longer)
        expectedMsg = (
            "not equal, lengths differ: 4 != 5\n"
            "  Array(1, 2, 3, 4)\n"
            "  Array(1, 2, 3, 4, 5)\n")
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)


    def testAssertEquals_ctypes_arrays_differ(self):
        one = (GLint * 4)(*[1, 2, 3, 4])
        different = (GLint * 4)(*[1, 2, 3, 5])
        assertion = lambda: self.mytestcase.assertEquals(one, different)
        expectedMsg = (
            "4 != 5 at index 3\n"
            "  Array(1, 2, 3, 4)\n"
            "  Array(1, 2, 3, 5)\n")
        self.mytestcase.assertRaises(assertion, AssertionError, expectedMsg)


    def testAssertEquals_sets(self):
        self.mytestcase.assertEquals(set(), set(), "empty sets should pass")

        one = set([2, 4, 6])
        two = set([6, 4, 2])
        self.mytestcase.assertEquals(one, two, "similar sets should pass")

        three = set([2, 4, 6, 8])
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertEquals(one, three, "desc"),
            AssertionError,
            "set([2, 4, 6]) != set([8, 2, 4, 6])\n  desc")

        four = set([2, 4])
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertEquals(one, four, "desc"),
            AssertionError,
            "set([2, 4, 6]) != set([2, 4])\n  desc")

        five = set([2, 4, 99])
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertEquals(one, five, "desc"),
            AssertionError,
            "set([2, 4, 6]) != set([2, 99, 4])\n  desc")


    def testAssertEquals_epsilon(self):
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertEquals (1.230, 1.239),
            AssertionError)

        self.mytestcase.assertEquals(1.23, 1.24, epsilon=0.011),
        self.mytestcase.assertEquals(1.24, 1.23, epsilon=0.011),

        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertEquals (1.23, 1.24001, epsilon=0.01),
            AssertionError)
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertEquals (1.24001, 1.23, epsilon=0.01),
            AssertionError)



class TestCase_assertRaises_test(RealTestCase):

    def setUp(self):
        self.mytestcase = ClassUnderTest("testAlwaysPasses")


    def testAssertRaises_for_func_that_raises_the_right_thing(self):

        def raiseCorrectly():
            raise ZeroDivisionError("actual message")

        self.mytestcase.assertRaises(
            raiseCorrectly, ZeroDivisionError, "actual message")


    def assertFailureModeOfAssertRaises( \
        self, func, expectedMsgIn, expectedMsgOut):

        try:
            self.mytestcase.assertRaises(
                func, ZeroDivisionError, expectedMsgIn)

        except AssertionError, e:
            if e.message != expectedMsgOut:
                message = \
                    "assertRaises should raise with correct message:\n" + \
                    "--actual message:----\n" + \
                    e.message + "\n" + \
                    "--expected message:----\n" + \
                    expectedMsgOut + "\n"
                self.fail(message)

        except Exception, e:
            self.fail("assertRaises should raise an AssertionError, not %s" % e)

        else:
            self.fail("assertRaises should raise")


    def testAssertRaises_for_func_that_raises_with_wrong_message(self):

        def raiseBadMessage():
            raise ZeroDivisionError("bad message")

        self.mytestcase.assertRaises(raiseBadMessage, ZeroDivisionError)

        expectedMsgOut = \
            "raised exception with wrong message:\n" + \
            "  bad message\n" + \
            "  expected message\n"
        self.assertFailureModeOfAssertRaises(
            raiseBadMessage, "expected message", expectedMsgOut)


    def testAssertRaises_for_func_that_doesnt_raise(self):

        def raiseNothing():
            pass

        expectedMsgOut = "didn't raise.\n" \
            "  Expected ZeroDivisionError(\"expected message\")"
        self.assertFailureModeOfAssertRaises( \
            raiseNothing, "expected message", expectedMsgOut)


    def testAssertRaises_for_fn_that_raises_wrong_exception_type(self):

        def raiseWrongType():
            raise TypeError("doesnt matter")

        expectedMsgOut = \
            "raised wrong exception type:\n" + \
            "  <type 'exceptions.TypeError'>(\"doesnt matter\")\n" + \
            "  <type 'exceptions.ZeroDivisionError'>"
        self.assertFailureModeOfAssertRaises(
            raiseWrongType, "expected message", expectedMsgOut)


    def testAssertRaises_returns_the_exception(self):

        e = ZeroDivisionError()

        def raisePlease():
            raise e

        actual = self.mytestcase.assertRaises(raisePlease, ZeroDivisionError)
        self.assertTrue(actual is e, "should return the raised exception")


    def assert_warns_on_bad_args(self, func, excClass, expectedPrefix):

        assertion = lambda: self.mytestcase.assertRaises(
            func, excClass, "WARNING")

        expectedMessage = (
            "%s" % expectedPrefix +
            "warning: assertRaises() in testutils/testcase.py has new sig:\n"
            "  assertRaises(self, func, expectedType, expectedMessage=None)")
        try:
            assertion()
        except Exception, e:
            self.assertEquals(type(e), TypeError,
                "should raise a TypeError, not: %s" % type(e))
            self.assertEquals(e.message, expectedMessage,
                "should raise with correct message, not: " + e.message)
        else:
            self.fail("should raise a warning")


    def testAssertRaises_warns_on_bad_args(self):

        def raisePlease():
            raise ZeroDivisionError

        arg1 = "1st arg is not callable\n"
        arg2 = "2nd arg is not exception class\n"
        self.assert_warns_on_bad_args(object(), ZeroDivisionError, arg1)
        self.assert_warns_on_bad_args(Exception, ZeroDivisionError, arg1)
        self.assert_warns_on_bad_args(raisePlease, object(), arg2)
        self.assert_warns_on_bad_args(raisePlease, lambda: None, arg2)
        self.assert_warns_on_bad_args(Exception, lambda: None, arg1+arg2)


class TestCase_assertVertsEqual(RealTestCase):

    def setUp(self):
        self.mytestcase = ClassUnderTest("testAlwaysPasses")

    def test_assertVertsEqual_equal(self):
        v1 = [(1, 2), (2, 3), (4, 5)]
        v2 = [(1, 2), (2, 3), (4, 5)]
        self.mytestcase.assertVertsEqual(v1, v2)
        self.mytestcase.assertVertsEqual(v1, v2, 'x')


    def test_assertVertsEqual_notequal(self):
        v1 = [(1, 2), (2, 3), (4, 5)]
        v2 = [(1, 2), (2, 3), (4, 66)]
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertVertsEqual(v1, v2),
            AssertionError,
            'verts differ at v2: (4, 5), (4, 66)\n')


    def test_assertVertsEqual_wronglen(self):
        v1 = [(1, 2), (2, 3)]
        v2 = [(1, 2), (2, 3), (4, 5)]
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertVertsEqual(v1, v2),
            AssertionError,
            'verts differ in len: 2, 3\n')


    def test_assertVertsEqual_badlyformed(self):
        v1 = [(1, 2), (3,)]
        v2 = [(1, 2), (2, 3)]
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertVertsEqual(v1, v2),
            AssertionError,
            'actual verts badly formed at v1: (3,)\n')

        v1 = [(1, 2), (3, 4), (5, 6)]
        v2 = [(1, 2), (3, 4), (5, 6, 7)]
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertVertsEqual(v1, v2),
            AssertionError,
            'expected verts badly formed at v2: (5, 6, 7)\n')


    def test_assertVertsEqual_degen(self):
        self.mytestcase.assertVertsEqual([], [])



class TestCase_assertValidColor_test(RealTestCase):

    def setUp(self):
        self.mytestcase = ClassUnderTest("testAlwaysPasses")


    def test_assertValidColor_with_valid_colors(self):
        self.mytestcase.assertValidColor((0, 0, 0))
        self.mytestcase.assertValidColor((255, 255, 255))
        self.mytestcase.assertValidColor((100, 100, 100), "msg")


    def assertBadColor(self, badColor):
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertValidColor(badColor),
            AssertionError,
            "bad color: %s\n" % (badColor,))
        self.mytestcase.assertRaises(
            lambda: self.mytestcase.assertValidColor(badColor, "msg"),
            AssertionError,
            "bad color: %s\nmsg" % (badColor,))


    def test_assertValidColor_raises_on_bad_color(self):
        self.assertBadColor((100, 100))
        self.assertBadColor((100, 100, 100, 100))
        self.assertBadColor((-1, 100, 100))
        self.assertBadColor((256, 100, 100))
        self.assertBadColor((100, -1, 100))
        self.assertBadColor((100, 256, 100))
        self.assertBadColor((100, 100, -1))
        self.assertBadColor((100, 100, 256))
        self.assertBadColor((100.0, 100, 100))
        self.assertBadColor((100, 100.0, 100))
        self.assertBadColor((100, 100, 100.0))




class combine_test(RealTestCase):

    def setUp(self):
        self.testIds = []

        class A_test(MyTestCase):
            def testOne(self2):
                self.testIds.append(1)
            def testTwo(self2):
                self.testIds.append(2)

        class B_test(MyTestCase):
            def testThree(self2):
                self.testIds.append(3)

        self.A_test = A_test
        self.B_test = B_test


    def assert_combine_behaviour(self, tests, expTestCount, expTestIds):

        combined = combine(*tests)

        self.assertTrue(isinstance(combined, TestSuite),
            "should return a TestSuite")
        numTestCases = combined.countTestCases()
        self.assertEquals(numTestCases, expTestCount,
            "should have %d test cases, had %s" % (expTestCount, numTestCases))

        class NullStream(object):
            def write(*args):
                pass

        TextTestRunner(stream=NullStream()).run(combined)
        self.assertEquals(self.testIds, expTestIds,
            "combined suite was %s, should be %s" % (self.testIds, expTestIds))


    def test_combine_nothing(self):
        self.assert_combine_behaviour([], 0, [])


    def test_combine_classes(self):
        self.assert_combine_behaviour([self.A_test, self.B_test], 3, [1, 2, 3])


    def test_combine_suites(self):
        loader = TestLoader()
        suite1 = loader.loadTestsFromTestCase(self.A_test)
        suite2 = loader.loadTestsFromTestCase(self.B_test)
        self.assert_combine_behaviour([suite1, suite2], 3, [1, 2, 3])


    def test_combine_classes_and_suites(self):
        loader = TestLoader()
        suite1 = loader.loadTestsFromTestCase(self.A_test)
        suite2 = loader.loadTestsFromTestCase(self.B_test)
        manyTests = [self.A_test, suite1, self.B_test, suite2]
        self.assert_combine_behaviour(manyTests, 6, [1, 2, 1, 2, 3, 3])


class run_test(MyTestCase):

    def test_passes_verbosity(self):
        mockRunner = Listener()
        mockRunner.return_value = TextTestRunner()
        mockRun = Listener()
        mockRunner.return_value.run = mockRun
        from solescion.testutils import testcase as testcase_module
        orig = testcase_module.TextTestRunner
        testcase_module.TextTestRunner = mockRunner
        try:
            suite = ClassUnderTest("testAlwaysPasses")
            run(suite, verbosity=33)
        finally:
            testcase_module.TextTestRunner = orig
        self.assertEquals(mockRunner.kwargs['verbosity'], 33,
            "didnt create a verbose runner")
        self.assertEquals(mockRun.args, (suite,), "didnt run suite")


TestCase_test = combine(
    TestCase_module_functions_test,
    TestCase_assertEquals_test,
    TestCase_assertRaises_test,
    TestCase_assertValidColor_test,
    TestCase_assertVertsEqual,
    combine_test,
    run_test,
)

if __name__ == "__main__":
    main()

