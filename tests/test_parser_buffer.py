# -*- coding: utf-8 -*-

from sora.parser import SizedParserBuffer
from sora.iobuffer import IOBuffer
from nose.tools import assert_equal

class TestSizedParserBuffer(object):

    def setUp(self):
        self.sizedParserBuffer = SizedParserBuffer(4)

    def test_add_data(self):
        assert_equal(True, self.sizedParserBuffer.add_data(IOBuffer('hello')))
        assert_equal('hell', self.sizedParserBuffer.result)

    def test_remaining(self):
        assert_equal(False, self.sizedParserBuffer.add_data(IOBuffer('hel')))
        assert_equal(3, self.sizedParserBuffer.received)

    def test_remaining(self):
        assert_equal(False, self.sizedParserBuffer.add_data(IOBuffer('hel')))
        assert_equal(1, self.sizedParserBuffer.remaining)

    def test_remaining(self):
        assert_equal(False, self.sizedParserBuffer.add_data(IOBuffer('hel')))
        assert_equal(False, self.sizedParserBuffer.is_finished)
        assert_equal(True, self.sizedParserBuffer.add_data(IOBuffer('lo')))
        assert_equal(True, self.sizedParserBuffer.is_finished)
