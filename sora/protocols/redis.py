# -*- coding: utf-8 -*-

from sora.parser import Byte, Bytes, BytesUntil, NoneParser, EmptyTupleParser

def simple_strings_parser():
    return BytesUntil('\r\n')

def errors_parser():
    return BytesUntil('\r\n')

def integers_parser():
    return BytesUntil('\r\n').then(lambda n: int(n))

def bulk_strings_parser():
    def help(n):
        if n >= 0:
            return Bytes(n).precombine(Bytes(2))
        if n < 0:
            return NoneParser()
    return BytesUntil('\r\n').link(lambda n: help(int(n)))

def arrays_parser():
    def help(n):
        parser = command_parser()
        if n < 0:
            return NoneParser()
        if n == 0:
            return EmptyTupleParser()
        if n == 1:
            return command_parser().then(lambda x: (x, ))
        if n > 1:
            for i in range(n-1):
                parser = parser.combine(command_parser())
            return parser
    return BytesUntil('\r\n').link(lambda n: help(int(n)))

def command_parser():
    def help(c):
        if c == '+':
            return simple_strings_parser()
        elif c == '-':
            return errors_parser()
        elif c == ':':
            return integers_parser()
        elif c == '$':
            return bulk_strings_parser()
        else:
            return arrays_parser()
    return Byte().link(lambda c: help(c))
