# -*- coding: utf-8 -*-

class SizedParserBuffer(object):
    """ Buffer sized data """
    def __init__(self, n):
        self.size = n
        self.buffer = ''
        self.received = 0

    @property
    def remaining(self):
        return self.size - self.received

    @property
    def is_finished(self):
        return self.size == self.received

    @property
    def result(self):
        return self.buffer

    def add_data(self, data):
        n = min(self.remaining, data.remaining)
        self.buffer += data.take(n)
        self.received += n
        if (self.remaining == 0):
            return True
        else:
            return False

    def reset(self):
        self.buffer = ''
        self.received = 0
