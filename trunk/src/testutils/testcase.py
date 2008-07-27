from unittest import TestCase as RealTestCase, TestLoader, TestSuite, main
from ctypes import Array


def _is_int_indexable(item):
    return (
        type(item) is not dict and
        hasattr(item, "__len__") and
        hasattr(item, "__getitem__")
    )


def _tostr(i):
    if isinstance(i, Array):
        return "Array(%s)" % ", ".join(str(x) for x in i)
    else:
        return str(i)


def _compare_lengths(actual, expected, message):
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


class MyTestCase(RealTestCase):

    def assertNone(self, item, message=None):
        if not item is None:
            if message is None:
                message = ""
            raise AssertionError("not None: %s\n  %s" % (item, message))


    def assertNotNone(self, item, message=None):
        if item is None:
            if message is None:
                message = ""
            raise AssertionError("is None\n  %s" % (message))


    def assertEquals(self, actual, expected, message=None):
        if message is None:
            message = ""

        if type(actual) != type(expected):
            # ctypes arrays of different length are actually different types
            # but reporting them as such is just confusing
            if not (isinstance(actual, Array) and isinstance(expected, Array)):
                msg = "not equal. types differ:\n  %s %s\n  %s %s\n%s" % \
                    (type(actual), actual, type(expected), expected, message)
                raise AssertionError(msg)

        if actual != expected:
            if _is_int_indexable(actual):
                _compare_indexables(actual, expected, message)
            else:
                msg = "%s != %s\n  %s" % (actual, expected, message)
                raise AssertionError(msg)


    def _assertRaises_test_args(self, fn, excClass):

        def isException(o):
            return isinstance(o, type) and issubclass(o, Exception)

        msg = ""
        arg1IsCallable = callable(fn) and not isException(fn)
        if not arg1IsCallable:
            msg += "1st arg is not callable\n"
        arg2IsExcClass = isException(excClass)
        if not arg2IsExcClass:
            msg += "2nd arg is not exception class\n"

        if not arg1IsCallable or not arg2IsExcClass:
            msg += (
            "warning: assertRaises() in testutils/testcase.py has new sig:\n"
            "  assertRaises(self, fn, expectedType, expectedMessage=None)")
            raise TypeError(msg)


    def assertRaises( \
        self, fn, expectedException, expectedMessage=None):

        self._assertRaises_test_args(fn, expectedException)

        try:
            fn()
        except expectedException, e:
            if expectedMessage is not None and e.message != expectedMessage:
                msg = "raised exception with wrong message:\n  %s\n  %s\n" % \
                    (e.message, expectedMessage)
                self.fail(msg)
        except Exception, e:
            msg = 'raised wrong exception type:\n  %s("%s")\n  %s' % \
                (type(e), e.message, expectedException)
            self.fail(msg)
        else:
            msg = "didn't raise.\n  Expected %s(\"%s\")" % \
                (expectedException.__name__, expectedMessage)
            self.fail(msg)
        return e


def combine(*args):
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


def run_test():
    main()

