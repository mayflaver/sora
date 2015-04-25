# -*- coding: utf-8 -*-

from sora.parser import SizedParserBuffer, UnsizedParserBuffer, Byte, Bytes
from sora.iobuffer import IOBuffer
from sora.datahandler import DataHandler
from nose.tools import assert_equal

class TestDataHandler(object):

    def setUp(self):
        self.result = ""
        def callback(data):
            self.result += data
        self.datahandler = DataHandler(Bytes(4), callback)

    def test_call(self):
        self.datahandler("hello world")
        assert_equal('hello wo', self.result)
        self.datahandler("s")
        assert_equal('hello worlds', self.result)
