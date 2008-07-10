from unittest import TestCase as RealTestCase, TestLoader, TestSuite, main
from ctypes import Array


def _stringifyIterable(i):
    if isinstance(i, Array):
        return "Array(%s)" % ", ".join(str(x) for x in i)
    else:
        return str(i)


class MyTestCase(RealTestCase):

    def _compareLengths(self, actual, expected, message):
        if len(actual) != len(expected):
            actualStr = _stringifyIterable(actual)
            expectedStr = _stringifyIterable(expected)
            msg = (
                "not equal, lengths differ: %d != %d\n"
                "  %s\n"
                "  %s\n"
                "%s" %
                (len(actual), len(expected), actualStr, expectedStr, message)
            )
            raise AssertionError(msg)

    def _compareIndexables(self, actual, expected, message):
        self._compareLengths(actual, expected, message)
        for index in range(len(actual)):
            if actual[index] != expected[index]:
                actualStr = _stringifyIterable(actual)
                expectedStr = _stringifyIterable(expected)
                msg = (
                    "not equal at index %d: %s != %s\n"
                    "  %s\n"
                    "  %s\n"
                    "%s" %
                    (index, actual[index], expected[index],
                        actualStr, expectedStr, message)
                )
                self.fail(msg)


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

        def isIndexable(item):
            return hasattr(actual, "__len__") and hasattr(actual, "__getitem__")

        if isIndexable(actual) and isIndexable(expected):
            self._compareIndexables(actual, expected, message)

        else:
            if actual != expected:
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
            self.fail("didn't raise")
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

