"module for the Listener class"

class Listener(object):
    """
    A Listener is a callable object, which records how many times it gets
    called, and with what arguments. It is useful for mocking out a
    callable during a unittest.
    """
    def __init__(self):
        self.argsList = None
        self.kwargsList = None
        self.returnValue = None
        self.returnValueList = []
        self.reset()

    def reset(self):
        "reset this instance as though it had just been created"
        self.argsList = []
        self.kwargsList = []

    triggered = property(lambda self: len(self.argsList) > 0)
    triggerCount = property(lambda self: len(self.argsList))

    def _get_args(self):
        "return args of the most recent call to this instance"
        if self.triggered:
            return self.argsList[-1]

    args = property(_get_args)

    def _get_kwargs(self):
        "return kwargs of the most recent call to this instance"
        if self.triggered:
            return self.kwargsList[-1]

    kwargs = property(_get_kwargs)

    def __call__(self, *args, **kwargs):
        self.argsList.append(args)
        self.kwargsList.append(kwargs)
        if self.returnValueList:
            return self.returnValueList.pop(0)
        else:
            return self.returnValue

