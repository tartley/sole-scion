class Listener(object):
    """
    A Listener is a callable object, which records how many times it gets
    called, and with what arguments. It is useful for mocking out a
    callable during a unittest.
    """
    def __init__(self, return_value=None, return_values=None):
        self.reset()

        self.return_value = return_value
        if return_values is None:
            return_values = []
        self.return_values = return_values

    def reset(self):
        # pylint: disable-msg=W0201
        #   Attribute defined outside __init__: ack
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
        if self.return_values:
            return self.return_values.pop(0)
        else:
            return self.return_value

