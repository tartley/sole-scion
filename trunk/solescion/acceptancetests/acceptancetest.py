from __future__ import division

from pyglet import app, clock

from solescion.testutils.testcase import MyTestCase


def get_windows():
    return [w for w in app.windows]


def get_window():
    windows = get_windows()
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


class AcceptanceTest(MyTestCase):
    """
    A TestCase which fires up the entire application, then proceeds to
    use pyglet's scheduler to evaluate a series of conditions on every
    gameloop frame. If all conditions evaluate to True, the test passes.
    If a condition evaluates to False, then it will be retried next frame.
    After it has been retried for 'timeout' seconds, the False condition
    will cause a test failure.
    """
    # pylint: disable-msg=R0904
    #   Too many public methods

    timeout = 1.0

    def __init__(self, *args):
        MyTestCase.__init__(self, *args)
        self.verbose = False
        self.conditions = None
        self.condition = None
        self.time = None


    def set_conditions(self, conditions):
        self.conditions = conditions
        self.next_condition()
        clock.schedule(lambda dt: self.try_condition(dt))


    def next_condition(self):
        if self.verbose:
            print "next_condition:",
        if len(self.conditions) > 0:
            self.condition = self.conditions.pop(0)
            if self.verbose:
                print self.condition.im_func.func_name
            self.time = 0.0
        else:
            self.terminate()


    def try_condition(self, delta_t):
        if self.verbose:
            print "try_condition"
        if self.condition():
            if self.verbose:
                print "  pass after %fs" % self.time
            self.next_condition()
        else:
            self.time += delta_t
            if self.time >= self.timeout:
                raise AssertionError("timeout on %s" % self.condition)


    def terminate(self):
        if self.verbose:
            print "terminate"
        win = get_window()
        win.has_exit = True

