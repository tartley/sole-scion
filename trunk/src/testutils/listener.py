
class Listener(object):

    def __init__(self):
        self.reset()
        self.returnValue = None
        self.returnValueList = []

    def reset(self):
        self.argsList = []
        self.kwargsList = []

    triggered = property(lambda self: len(self.argsList) > 0)
    triggerCount = property(lambda self: len(self.argsList))

    def _getArgs(self):
        if self.triggered:
            return self.argsList[-1]

    args = property(_getArgs)

    def _getKwargs(self):
        if self.triggered:
            return self.kwargsList[-1]

    kwargs = property(_getKwargs)

    def __call__(self, *args, **kwargs):
        self.argsList.append(args)
        self.kwargsList.append(kwargs)
        if self.returnValueList:
            return self.returnValueList.pop(0)
        else:
            return self.returnValue

