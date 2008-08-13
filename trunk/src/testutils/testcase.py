"Provides class 'MyTestCase', 'combine()' and 'run_test()'"

from ctypes import Array
from unittest import (
    TestCase as RealTestCase, TestLoader, TestSuite, TextTestRunner
)


def _is_int_indexable(item):
    "Return true if item is indexable with integers"
    return (
        type(item) is not dict and
        hasattr(item, "__len__") and
        hasattr(item, "__getitem__")
    )


def _tostr(item):
    "Convert item to str, special casing types with rubbish defaults"
    if isinstance(item, Array):
        return "Array(%s)" % ", ".join(str(x) for x in item)
    else:
        return str(item)


def _compare_lengths(actual, expected, message):
    "Fail with a useful message if lengths differ"
    if len(actual) != len(expected):
        actualStr = _tostr(actual)
        expectedStr = _tostr(expected)
        msg = (
            "not equal, lengths differ: %d != %d\n"
            "  %s\n"
            "  %s\n"
            "%s" %
            (len(actual), len(expected), actualStr, expectedStr, message)
        )
        raise AssertionError(msg)


def _compare_indexables(actual, expected, message):
    "Fail with a useful message if content of indexable items differs"
    _compare_lengths(actual, expected, message)
    for index in range(len(actual)):
        if actual[index] != expected[index]:
            actualStr = _tostr(actual)
            expectedStr = _tostr(expected)
            msg = (
                "%s != %s at index %d\n"
                "  %s\n"
                "  %s\n"
                "%s" %
                (actual[index], expected[index], index,
                    actualStr, expectedStr, message)
            )
            raise AssertionError(msg)


def _compare_types(actual, expected, message):
    """
    Fail if types differ, except in a few special cases where different
    types are considered to be the same (eg Vec2d and tuple of 2)
    """
    if type(actual) == type(expected):
        return

    # ctypes arrays of different length are actually different types
    # but reporting them as such is just confusing
    if isinstance(actual, Array) and isinstance(expected, Array):
        return

    msg = "not equal. types differ:\n  %s %s\n  %s %s\n%s" % \
        (type(actual), actual, type(expected), expected, message)
    raise AssertionError(msg)


class MyTestCase(RealTestCase):
    "A TestCase with augmented assertions"
    # pylint: disable-msg=C0103
    #   Invalid method names: This class uses unittest.TestCase conventions
    # pylint: disable-msg=R0904
    #   Too many public methods

    def assertNone(self, item, message=None):
        "Fail if item is not None"
        if not item is None:
            if message is None:
                message = ""
            raise AssertionError("not None: %s\n  %s" % (item, message))


    def assertNotNone(self, item, message=None):
        "Fail if item is None"
        if item is None:
            if message is None:
                message = ""
            raise AssertionError("is None\n  %s" % (message))


    def assertEquals(self, actual, expected, message=None):
        "Fail with useful message if actual is not equal expected"
        if message is None:
            message = ""

        _compare_types(actual, expected, message)

        if actual != expected:
            if _is_int_indexable(actual):
                _compare_indexables(actual, expected, message)
            else:
                msg = "%s != %s\n  %s" % (actual, expected, message)
                raise AssertionError(msg)


    def assertValidColor(self, color, message=None):
        "Fails if color is not a triplet of ints from 0 to 255"
        if message is None:
            message = ""
        if len(color) != 3:
            self.fail("bad color: %s\n%s" % (color, message))
        for i in [0, 1, 2]:
            cpt = color[i]
            if not isinstance(cpt, int) or not 0 <= cpt <= 255:
                self.fail("bad color: %s\n%s" % (color, message))


    def _assertRaises_test_args(self, func, excClass):
        "Raise TypeError on bad args to assertRaises"

        def is_exception(obj):
            "return true if obj is an Exception class"
            return isinstance(obj, type) and issubclass(obj, Exception)

        msg = ""
        arg1IsCallable = callable(func) and not is_exception(func)
        if not arg1IsCallable:
            msg += "1st arg is not callable\n"
        arg2IsExcClass = is_exception(excClass)
        if not arg2IsExcClass:
            msg += "2nd arg is not exception class\n"

        if not arg1IsCallable or not arg2IsExcClass:
            msg += (
            "warning: assertRaises() in testutils/testcase.py has new sig:\n"
            "  assertRaises(self, func, expectedType, expectedMessage=None)")
            raise TypeError(msg)


    def assertRaises( \
        self, func, expectedException, expectedMessage=None):
        "Fail if func doesn't raise expectedException"

        self._assertRaises_test_args(func, expectedException)

        try:
            func()
        except expectedException, actual:
            messageWrong = (
                expectedMessage is not None and \
                actual.message != expectedMessage)
            if messageWrong:
                msg = "raised exception with wrong message:\n  %s\n  %s\n" % \
                    (actual.message, expectedMessage)
                self.fail(msg)
        except Exception, actual:
            msg = 'raised wrong exception type:\n  %s("%s")\n  %s' % \
                (type(actual), actual.message, expectedException)
            self.fail(msg)
        else:
            msg = "didn't raise.\n  Expected %s(\"%s\")" % \
                (expectedException.__name__, expectedMessage)
            self.fail(msg)
        return actual


def combine(*args):
    "combine given list of TestCase classes and suite objects into a new suite"
    loader = TestLoader()
    suites = []
    for arg in args:
        if isinstance(arg, TestSuite):
            suites.append(arg)
        elif issubclass(arg, RealTestCase):
            suites.append(loader.loadTestsFromTestCase(arg))
        else:
            msg = "combine: bad arg type: %s <%s>" % (arg, type(arg))
            raise AssertionError(msg)
    return TestSuite(suites)


def run_test(suite, verbosity=1):
    "Use a TextTestRunner to run the given test suite"
    if isinstance(suite, type) and issubclass(suite, RealTestCase):
        suite = TestLoader().loadTestsFromTestCase(suite)
    TextTestRunner(verbosity=verbosity).run(suite)


