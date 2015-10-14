

class CallRecorder(object):
    """
    A very simple helper to record what calls it got
    """

    def __init__(self):
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append([args, kwargs])
