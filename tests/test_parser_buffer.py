# -*- coding: utf-8 -*-

from sora.parser import *
from sora.iobuffer import IOBuffer
from nose.tools import assert_equal, assert_is

class TestUncomplete(object):
    def setUp(self):
        self.Uncomplete1 = Uncomplete()
        self.Uncomplete2 = Uncomplete()

    def test_is_Uncomplete(self):
        assert_is(self.Uncomplete1, self.Uncomplete2)

        
class TestSizedParserBuffer(object):

    def setUp(self):
        self.sizedParserBuffer = SizedParserBuffer(4)

    def test_add_data(self):
        assert_equal(True, self.sizedParserBuffer.add_data(IOBuffer('hello')))
        assert_equal('hell', self.sizedParserBuffer.result)

    def test_received(self):
        assert_equal(False, self.sizedParserBuffer.add_data(IOBuffer('hel')))
        assert_equal(3, self.sizedParserBuffer.received)

    def test_remaining(self):
        assert_equal(False, self.sizedParserBuffer.add_data(IOBuffer('hel')))
        assert_equal(1, self.sizedParserBuffer.remaining)

    def test_is_finished(self):
        assert_equal(False, self.sizedParserBuffer.add_data(IOBuffer('hel')))
        assert_equal(False, self.sizedParserBuffer.is_finished)
        assert_equal(True, self.sizedParserBuffer.add_data(IOBuffer('lo')))
        assert_equal(True, self.sizedParserBuffer.is_finished)

    def test_equal(self):
        assert_equal(self.sizedParserBuffer, SizedParserBuffer(4))

    def test_reset(self):
        self.sizedParserBuffer.add_data(IOBuffer('hel'))
        self.sizedParserBuffer.reset()
        assert_equal(self.sizedParserBuffer, SizedParserBuffer(4))


class TestUnsizedParserBufferUnincludeTerminal(object):

    def setUp(self):
        self.unsizedParserBufferUnincludeTerminal = UnsizedParserBuffer("foo")

    def test_add_data(self):
        assert_equal(False, self.unsizedParserBufferUnincludeTerminal.add_data(IOBuffer("somef")))
        assert_equal(True, self.unsizedParserBufferUnincludeTerminal.add_data(IOBuffer("foos")))
        assert_equal("somef", self.unsizedParserBufferUnincludeTerminal.result)

    def test_equal(self):
        assert_equal(self.unsizedParserBufferUnincludeTerminal, UnsizedParserBuffer("foo"))

    def test_reset(self):
        self.unsizedParserBufferUnincludeTerminal.add_data(IOBuffer("somef"))
        self.unsizedParserBufferUnincludeTerminal.reset()
        assert_equal(self.unsizedParserBufferUnincludeTerminal, UnsizedParserBuffer("foo"))

                     
class TestUnsizedParserBufferIncludeTerminal(object):
    
    def setUp(self):
        self.unsizedParserBufferIncludeTerminal = UnsizedParserBuffer("foo", True)
        
    def test_add_data(self):
        assert_equal(False, self.unsizedParserBufferIncludeTerminal.add_data(IOBuffer("somef")))
        assert_equal(True, self.unsizedParserBufferIncludeTerminal.add_data(IOBuffer("oos")))
        assert_equal("somefoo", self.unsizedParserBufferIncludeTerminal.result)

    def test_equal(self):
        assert_equal(self.unsizedParserBufferIncludeTerminal, UnsizedParserBuffer("foo", True))

    def test_reset(self):
        self.unsizedParserBufferIncludeTerminal.add_data(IOBuffer("somef"))
        self.unsizedParserBufferIncludeTerminal.reset()
        assert_equal(self.unsizedParserBufferIncludeTerminal, UnsizedParserBuffer("foo", True))


class TestUnsizedParserBufferSkiped(object):
    
    def setUp(self):
        self.unsizedParserBufferSkiped = UnsizedParserBuffer("foo", False, 2)

    def test_add_data(self):
        assert_equal(False, self.unsizedParserBufferSkiped.add_data(IOBuffer("somef")))
        assert_equal(True, self.unsizedParserBufferSkiped.add_data(IOBuffer("oos")))
        assert_equal("me", self.unsizedParserBufferSkiped.result)

    def test_equal(self):
        assert_equal(self.unsizedParserBufferSkiped, UnsizedParserBuffer("foo", False, 2))

    def test_reset(self):
        self.unsizedParserBufferSkiped.add_data(IOBuffer("somef"))
        self.unsizedParserBufferSkiped.reset()
        assert_equal(self.unsizedParserBufferSkiped, UnsizedParserBuffer("foo", False, 2))

        
class TestByte(object):

    def setUp(self):
        self.parser = Byte()

    def test_parser(self):
        data = IOBuffer('hi')
        assert_equal('h', self.parser.parser(data))
        assert_equal('i', self.parser.parser(data))
        assert_equal(Uncomplete(), self.parser.parser(data))


class TestNoneParser(object):
    def setup(self):
        self.parser = NoneParser()

    def test_parser(self):
        data = IOBuffer('bar')
        assert_equal(None, self.parser.parser(data))

class TestEmptyTupleParser(object):
    def setup(self):
        self.parser = EmptyTupleParser()

    def test_parser(self):
        data = IOBuffer('bar')
        assert_equal((), self.parser.parser(data))


class TestBytes(object):

    def setUp(self):
        self.parser = Bytes(4)

    def test_parser(self):
        data = IOBuffer('hello world')
        assert_equal('hell', self.parser.parser(data))
        assert_equal('o wo', self.parser.parser(data))
        assert_equal(Uncomplete(), self.parser.parser(data))


class TestShort(object):

    def setUp(self):
        self.parser = Short()

    def test_parser(self):
        data1 = IOBuffer('\xff')
        assert_equal(Uncomplete(), self.parser.parser(data1))
        data2 = IOBuffer('\xff')
        assert_equal(-1, self.parser.parser(data2))


class TestUnsignedShort(object):

    def setUp(self):
        self.parser = UnsignedShort()

    def test_parser(self):
        data1 = IOBuffer('\xff')
        assert_equal(Uncomplete(), self.parser.parser(data1))
        data2 = IOBuffer('\xff')
        assert_equal(2**16-1, self.parser.parser(data2))


class TestInt(object):

    def setUp(self):
        self.parser = Int()

    def test_parser(self):
        data1 = IOBuffer('\xff')
        assert_equal(Uncomplete(), self.parser.parser(data1))

        data2 = IOBuffer('\xff\xff\xff')
        assert_equal(-1, self.parser.parser(data2))


class TestUnsignedInt(object):

    def setUp(self):
        self.parser = UnsignedInt()

    def test_parser(self):
        data1 = IOBuffer('\xff')
        assert_equal(Uncomplete(), self.parser.parser(data1))
        data2 = IOBuffer('\xff\xff\xff')
        assert_equal(2**32-1, self.parser.parser(data2))


class TestLong(object):

    def setUp(self):
        self.parser = Long()

    def test_parser(self):
        data1 = IOBuffer('\xff\xff\xff\xff')
        assert_equal(Uncomplete(), self.parser.parser(data1))
        data2 = IOBuffer('\xff\xff\xff\xff')
        assert_equal(-1, self.parser.parser(data2))


class TestUnsignedLong(object):

    def setUp(self):
        self.parser = UnsignedLong()

    def test_parser(self):
        data1 = IOBuffer('\xff\xff\xff\xff')
        assert_equal(Uncomplete(), self.parser.parser(data1))
        data2 = IOBuffer('\xff\xff\xff\xff')
        assert_equal(2**64-1, self.parser.parser(data2))


class TestBytesUntil(object):

    def setUp(self):
        self.parser = BytesUntil("\n")

    def test_parser(self):
        data1 = IOBuffer("hello")
        assert_equal(Uncomplete(), self.parser.parser(data1))
        data2 = IOBuffer("\nworld\n")
        assert_equal('hello', self.parser.parser(data2))
        assert_equal('world', self.parser.parser(data2))

        
class TestCombine(object):

    def setUp(self):
        self.parser = Bytes(4).combine(Bytes(4))

    def test_parser(self):
        data = IOBuffer('hello world')
        assert_equal(('hell', 'o wo'), self.parser.parser(data))
        assert_equal(Uncomplete(), self.parser.parser(data))


class TestPreCombine(object):

    def setUp(self):
        self.parser = Bytes(4).precombine(Bytes(4))

    def test_parser(self):
        data = IOBuffer('hello world')
        assert_equal('hell', self.parser.parser(data))
        assert_equal(Uncomplete(), self.parser.parser(data))


class TestSufCombine(object):

    def setUp(self):
        self.parser = Bytes(4).sufcombine(Bytes(4))

    def test_parser(self):
        data = IOBuffer('hello world')
        assert_equal('o wo', self.parser.parser(data))
        assert_equal(Uncomplete(), self.parser.parser(data))


class TestThen(object):

    def setUp(self):
        self.parser = Bytes(2).then(lambda x: x*3)

    def test_parser(self):
        data1 = IOBuffer('h')
        assert_equal(Uncomplete(), self.parser.parser(data1))
        data2 = IOBuffer('ello world')
        assert_equal('hehehe', self.parser.parser(data2))

class TestLink(object):

    def setUp(self):
        self.parser = Bytes(2).link(lambda x: Bytes(2))

    def test_parser(self):
        data1 = IOBuffer('hel')
        assert_equal(Uncomplete(), self.parser.parser(data1))
        data2 = IOBuffer('l')
        assert_equal('ll', self.parser.parser(data2))
