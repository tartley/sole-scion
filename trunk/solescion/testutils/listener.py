class Listener(object):
    """
    A Listener is a callable object, which records how many times it gets
    called, and with what arguments. It is useful for mocking out a
    callable during a unittest.
    """
    def __init__(self):
        self.args_list = None
        self.kwargs_list = None
        self.return_value = None
        self.return_value_list = []
        self.reset()

    def reset(self):
        self.args_list = []
        self.kwargs_list = []

    triggered = property(lambda self: len(self.args_list) > 0)
    triggerCount = property(lambda self: len(self.args_list))

    def _get_args(self):
        if self.triggered:
            return self.args_list[-1]

    args = property(_get_args)

    def _get_kwargs(self):
        if self.triggered:
            return self.kwargs_list[-1]

    kwargs = property(_get_kwargs)

    def __call__(self, *args, **kwargs):
        self.args_list.append(args)
        self.kwargs_list.append(kwargs)
        if self.return_value_list:
            return self.return_value_list.pop(0)
        else:
            return self.return_value

