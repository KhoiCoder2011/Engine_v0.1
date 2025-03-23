import time


class Time:
    def __init__(self):
        self._start = 0
        self._end = 0
        self.time = 0

    def start(self):
        self._start = time.time()

    def end(self):
        self._end = time.time()

    def get_time(self):
        return self._end - self._start
