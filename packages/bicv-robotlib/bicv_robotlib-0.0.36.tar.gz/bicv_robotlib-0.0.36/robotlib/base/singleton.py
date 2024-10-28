import threading

class Singleton:
    instance = None
    lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            with cls.lock:
                if cls.instance is None:
                    cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        pass