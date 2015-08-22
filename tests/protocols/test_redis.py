from sora.iobuffer import IOBuffer
from sora.protocols.redis import command_parser
from nose.tools import assert_equal

class TestRedis(object):

    def setUp(self):
        self.parser = command_parser()

    def test_simple_strings_parser(self):
        data = IOBuffer('+OK\r\n')
        assert_equal('OK', self.parser.parser(data))

    def test_errors_parser(self):
        data = IOBuffer('-Error message\r\n')
        assert_equal('Error message', self.parser.parser(data))

    def test_integers_parser(self):
        data = IOBuffer(':0\r\n')
        assert_equal(0, self.parser.parser(data))

    def test_bulk_strings_parser(self):
        data = IOBuffer('$6\r\nfoobar\r\n')
        assert_equal('foobar', self.parser.parser(data))

    def test_array_string_parser(self):
        # empty array
        data0 = IOBuffer('*0\r\n')
        assert_equal(None, self.parser.parser(data0))
        # array with 1 element
        data1 = IOBuffer('*1\r\n$3\r\nfoo\r\n')
        assert_equal(('foo',), self.parser.parser(data1))
        # array with >1 element
        data2 = IOBuffer('*2\r\n$3\r\nfoo\r\n$3\r\n')
        assert_equal(None, self.parser.parser(data2))
        data3 = IOBuffer('bar\r\n')
        assert_equal(('foo', 'bar'), self.parser.parser(data3))

