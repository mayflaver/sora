# -*- coding: utf-8 -*-
from sora.iobuffer import IOBuffer
from sora.parser import Uncomplete

class DataHandler(object):
    """ parser data and pass to callback """
    def __init__(self, parser, callback):
        self.parser = parser
        self.callback = callback
        self.buffer = None

    def __call__(self, data):
        if (self.buffer is None):
            self.buffer = IOBuffer(data)
        else:
            self.buffer = IOBuffer(self.buffer.take_all+data)
        while 1:
            result = self.parser.parser(self.buffer)
            if result is not Uncomplete():
                self.callback(result)
            else:
                break
