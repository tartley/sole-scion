"Module for class 'AcceptanceTest'"
from __future__ import division

from testutils.testcase import MyTestCase

from pyglet import app, clock


class AcceptanceTest(MyTestCase):
    """
    A TestCase which fires up the entire application, then proceeds to
    use pyglet's scheduler to evaluate a series of conditions on every
    gameloop frame. If all conditions evaluate to True, the test passes.
    If a condition evaluates to False, then it will be retried next frame.
    After it has been retried for 'timeout' seconds, the False condition
    will cause a test failure.
    """

    timeout = 1.0

    def __init__(self, *args):
        MyTestCase.__init__(self, *args)
        self.verbose = False
        self.conditions = None
        self.condition = None
        self.time = None


    def set_conditions(self, conditions):
        "Set the list of conditions to be evaluated during this test"
        self.conditions = conditions
        self.next_condition()
        clock.schedule(lambda dt: self.try_condition(dt))


    def next_condition(self):
        """
        Obtain the next current condition to be evaluated.
        If there are no conditions left, the test has passed.
        """
        if self.verbose:
            print "next_condition:",
        if len(self.conditions) > 0:
            self.condition = self.conditions.pop(0)
            if self.verbose:
                print self.condition.im_func.func_name
            self.time = 0.0
        else:
            self.terminate()


    def try_condition(self, deltaT):
        """
        Test the current condition. If it passes, get the next one.
        If it fails and the timeout has been exceeded, fail.
        """

        if self.verbose:
            print "try_condition"
        if self.condition():
            if self.verbose:
                print "  pass after %fs" % self.time
            self.next_condition()
        else:
            self.time += deltaT
            if self.time >= self.timeout:
                raise AssertionError("timeout on %s" % self.condition)


    def get_windows(self):
        "Utility to return all open Pyglet windows"
        return [w for w in app.windows]


    def get_window(self):
        """
        Utility to return a single open Pyglet window.
        Fails if more than one window is open.
        """
        windows = self.get_windows()
        if len(windows) == 1:
            return windows[0]
        elif len(windows) == 0:
            return None
        else:
            msg = (
                "%d windows open:\n  " + \
                '\n  '.join(win.caption for win in windows)) \
                % (len(windows),)
            raise AssertionError(msg)


    def terminate(self):
        "End the program under test by closing its Pyglet window."
        if self.verbose:
            print "terminate"
        win = self.get_window()
        win.has_exit = True

