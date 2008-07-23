from __future__ import division

from testutils.testcase import MyTestCase

from pyglet import app, clock


class AcceptanceTest(MyTestCase):

    timeout = 1.0

    def __init__(self, *args):
        MyTestCase.__init__(self, *args)
        self.verbose = False


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


    def try_condition(self, dt):
        if self.verbose:
            print "try_condition"
        if self.condition():
            if self.verbose:
                print "  pass after %fs" % self.time
            self.next_condition()
        else:
            self.time += dt
            if self.time >= self.timeout:
                raise AssertionError("timeout on %s" % self.condition)


    def get_windows(self):
        return [w for w in app.windows]


    def get_window(self):
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
        if self.verbose:
            print "terminate"
        win = self.get_window()
        win.has_exit = True
