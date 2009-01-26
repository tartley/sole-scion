from ctypes import Array
from types import FloatType
from unittest import (
    TestCase as RealTestCase, TestLoader, TestSuite, TextTestRunner,
)

from .ColoredStream import ColoredStream


def _is_int_indexable(item):
    return (
        type(item) is not dict and
        hasattr(item, "__len__") and
        hasattr(item, "__getitem__")
    )


def _tostr(item):
    if isinstance(item, Array):
        return "Array(%s)" % ", ".join(str(x) for x in item)
    else:
        return str(item)


def _compare_lengths(actual, expected, message):
    if len(actual) != len(expected):
        actual_str = _tostr(actual)
        expected_str = _tostr(expected)
        msg = (
            "not equal, lengths differ: %d != %d\n"
            "  %s\n"
            "  %s\n"
            "%s" %
            (len(actual), len(expected), actual_str, expected_str, message)
        )
        raise AssertionError(msg)


def _compare_scalars(actual, expected, epsilon):
    if isinstance(actual, FloatType):
        return abs(actual - expected) <= epsilon
    else:
        return actual == expected


def _compare_indexables(actual, expected, message):
    _compare_lengths(actual, expected, message)
    for index in range(len(actual)):
        if actual[index] != expected[index]:
            actual_str = _tostr(actual)
            expected_str = _tostr(expected)
            msg = (
                "%s != %s at index %d\n"
                "  %s\n"
                "  %s\n"
                "%s" %
                (actual[index], expected[index], index,
                    actual_str, expected_str, message)
            )
            raise AssertionError(msg)


def _compare_types(actual, expected, message):
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
    # pylint: disable-msg=C0103
    #   Invalid method names: This class uses unittest.TestCase conventions
    # pylint: disable-msg=R0904
    #   Too many public methods: we are a subclass of unittest.TestCase
    # pylint: disable-msg=R0201
    #   Method could be a function: acknowledged.

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


    def assertEquals(self, actual, expected, message=None, epsilon=0):
        if message is None:
            message = ""

        _compare_types(actual, expected, message)

        if _is_int_indexable(actual):
            _compare_indexables(actual, expected, message)
        else:

            passed = _compare_scalars(actual, expected, epsilon)
            if not passed:
                msg = "%s != %s\n  %s" % (actual, expected, message)
                raise AssertionError(msg)


    def assertValidColor(self, color, message=None):
        if message is None:
            message = ""
        if len(color) != 3:
            self.fail("bad color: %s\n%s" % (color, message))
        for i in [0, 1, 2]:
            cpt = color[i]
            if not isinstance(cpt, int) or not 0 <= cpt <= 255:
                self.fail("bad color: %s\n%s" % (color, message))


    def assertVertsEqual(self, actual, expected, message=None):
        if len(actual) != len(expected):
            self.fail('verts differ in len: %d, %d'
                % (len(actual), len(expected)))

        for index in xrange(len(actual)):
            a = actual[index]
            e = expected[index]

            if len(a) != 2:
                self.fail('actual verts badly formed at v%d: %s'
                    % (index, a))
            if len(e) != 2:
                self.fail('expected verts badly formed at v%d: %s'
                    % (index, e))

            if not (
                _compare_scalars(a[0], e[0], epsilon=10**-6)
                and
                _compare_scalars(a[1], e[1], epsilon=10**-6)
                ):

                self.fail('verts differ at v%d: %s, %s' % (index, a, e))


    def _assertRaises_test_args(self, func, excClass):

        def is_exception(obj):
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
    "combine given TestCase classes and suite objects into a new suite"
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


def run(suite, verbosity=2):

    from solescion.testutils.TerminalController import TerminalController
    term = TerminalController()

    highlights = [
        ['^Ran \d+ tests in \d+\.\d+s$', term.WHITE+ term.BOLD],
        ['^OK$', term.GREEN + term.BOLD],
        ['ok$', term.GREEN + term.BOLD],
        ['^=+$', term.BLACK + term.BOLD],
        ['^-+$', term.BLACK + term.BOLD],
        [' \(.*\)$', term.BLACK + term.BOLD],
        ['^ \.\.\. $', term.BLACK + term.BOLD],
        ['^ERROR: ', term.RED + term.BOLD],
        ['^FAIL: ', term.YELLOW+ term.BOLD],
        ['FAIL$', term.YELLOW+ term.BOLD],
        ['ERROR$', term.RED + term.BOLD],
    ]
    stream = ColoredStream(highlights)

    if isinstance(suite, type) and issubclass(suite, RealTestCase):
        suite = TestLoader().loadTestsFromTestCase(suite)
    TextTestRunner(stream=stream, verbosity=verbosity).run(suite)

