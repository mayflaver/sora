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

    def __eq__(self, other):
        return self.buffer == other.buffer and self.received == other.received


class UnsizedParserBuffer(object):
    """ unsized parser buffer """
    def __init__(self, terminal, include=False, skip=0):
        self.terminal = terminal
        self.include = include
        self.skip = skip
        self.data = ''
        self.skiped = 0
        self.check_index = 0

    def _add_byte(self, byte):
        if (self.skiped < self.skip):
            self.skiped += 1
            return False
        
        elif (byte == self.terminal[self.check_index]):
            if (self.include):
                self.data += byte
            if (self.check_index == len(self.terminal)-1):
                return True
            else:
                self.check_index += 1
                return False
        else:
            if (self.check_index != 0):
                if (not self.include):
                    self.data += self.terminal[0:self.check_index]
                self.check_index = 0
            self.data += byte
            return False

    def add_data(self, data):
        last = False
        while (data.has_next and not last):
            last = self._add_byte(data.next)
        return last

    @property
    def result(self):
        return self.data

    def reset(self):
        self.data = ''
        self.skiped = 0
        self.check_index = 0

    def __eq__(self, other):
        return self.terminal == other.terminal \
            and self.include == other.include \
            and self.skip == other.skip \
            and self.data == other.data \
            and self.skiped == other.skiped \
            and self.check_index == other.check_index


class Parser(object):
    def parser(self, data):
        raise NotImplementedError()


class Byte(Parser):
    """ parser one byte """
    def parser(self, data):
        if (data.has_next):
            return data.next
        else:
            return None

class Bytes(Parser):
    """ parser multi bytes """
    def __init__(self, n):
        self.buffer = SizedParserBuffer(n)
        
    def parser(self, data):
        result = ''
        if (self.buffer.add_data(data)):
            result = self.buffer.result
            self.buffer.reset()
            return result
        else:
            return None
