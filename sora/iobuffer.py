# -*- coding: utf-8 -*-

class IOBuffer:
    """ IOBuffers are the simple way that data is read from and written to a
    connection.  IOBuffers are mutable and not thread safe.  They can only be
    read from once and cannot be reset.
    """
    def __init__(self, data):
        self.data = data
        self.read = 0

    @property
    def next(self):
        """Get the next byte, removing it from the buffer. warning:  This
        method will throw an exception if no data is left.
        """
        byte, self.data = self.data[:1], self.data[1:]
        self.read += 1
        return byte

    def take(self, n):
        """Get some bytes"""
        size = min(n, self.remaining)
        self.read += size
        bytes, self.data = self.data[:size], self.data[size:]
        return bytes

    @property
    def take_all(self):
        """Get all bytes"""
        return self.take(self.remaining)

    @property
    def remaining(self):
        return len(self.data)

    @property
    def take_copy(self):
        """Copy the unread data in this buffer to a new buffer"""
        return IOBuffer(self.take_all)

    def write_to(self, s):
        """write data to socket"""
        n = s.write(self.data)
        self.data = self.data[n:]

    @property
    def has_next(self):
        """Returns true if this IoBuffer still has unread data, false otherwise"""
        return self.remaining != 0

    @property
    def taken(self):
        """Returns how many bytes have already been read"""
        return self.read

    def skip(self, n):
        if (n <= self.remaining):
            self.read += n
            self.data = self.data[n:]
        else:
            self.read += self.remaining
            self.data = self.data[self.remaining:]

    def skip_all(self):
        self.skip(self.remaining)

    def __eq__(self, other):
        return self.take_all == other.take_all
