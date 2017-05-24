"""
Asyncit module
"""
from threading import Thread, Event


class Awaiter(object):
    """
    Awaiter class
    """
    handlers = {}
    queue = {}

    @staticmethod
    def wait(signal_name):
        """
        Wait for signal
        """
        if signal_name in Awaiter.queue:
            Awaiter.queue[signal_name] -= 0
        else:
            Awaiter.handlers[signal_name] = Event()
            Awaiter.handlers[signal_name].wait()

    @staticmethod
    def post(signal_name):
        """
        Post a signal
        """
        if signal_name in Awaiter.handlers:
            Awaiter.handlers[signal_name].set()
        else:
            Awaiter.handlers[signal_name] = Event()
            Awaiter.queue[signal_name] += 1


class Deferit(Thread):
    """
    Thread class
    """
    def __init__(self, method, *args):
        """
        Initialize the thread
        """
        self.method = method
        self.args = args

    def wait(self):
        """
        Start the thread
        """
        method_name_hash = hash(self.method.__name__)
        def f_star(*args):
            """
            Function wrapper
            """
            results = args[1]
            try:
                if args[0] == ():
                    result = self.method()
                else:
                    result = self.method(*args[0])
                results[0] = result
                Awaiter.post(method_name_hash)
            except Exception:
                Awaiter.post(method_name_hash)
                raise
        results = [None]
        Thread.__init__(self, target=f_star, args=[self.args, results])
        self.start()
        Awaiter.wait(method_name_hash)
        return results[0]

    def nowait(self, func=None):
        """
        Start the thread without waiting
        """
        def f_star(*args):
            """
            Function wrapper
            """
            func = args[1]
            if args[0] == ():
                result = self.method()
            else:
                result = self.method(*args[0])
            if func:
                func(result)
        Thread.__init__(self, target=f_star, args=[self.args, func])
        self.start()


class Asyncit(object):
    """
    Await/Defer decorator wrappers
    """

    @staticmethod
    def wait(func):
        """
        Wait decorator
        """
        def wrapper(*args):
            """
            Wait decorator wrapper
            """
            return Deferit(func, *args).wait()
        return wrapper

    @staticmethod
    def nowait(func):
        """
        Nowait decorator
        """
        def wrapper(*args):
            """
            Nowait decorator wrapper
            """
            return Deferit(func, *args).nowait
        return wrapper
