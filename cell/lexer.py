
import re

from cell.assert_implements import assert_implements
from cell.iterator import Iterator


def _is_number_or_decimal_point(c):
    return c is not None and re.match("[.0-9]", c)


def _scan(first_char, chars_p, allowed):
    assert type(chars_p) is PeekableStream
    ret = first_char
    p = chars_p.peek
    while p is not None and re.match(allowed, p):
        ret += chars_p.next()
        p = chars_p.peek
    return ret


def _scan_string(delim, chars_p):
    assert type(chars_p) is PeekableStream
    ret = ""
    while chars_p.peek != delim:
        c = chars_p.next()
        if c is None:
            raise Exception("A string ran off the end of the program!")
        ret += c
    chars_p.next()
    return ret


class PeekableStream:
    """
    Turns an iterator into something we can peek ahead one item of.
    """

    def __init__(self, iterator):
        assert_implements(iterator, Iterator)
        self.iterator = iter(iterator)
        self._fill()

    def _fill(self):
        try:
            self.peek = self.iterator.__next__()
        except StopIteration:
            self.peek = None

    def next(self):
        ret = self.peek
        self._fill()
        return ret


def lex(chars):
    assert_implements(chars, Iterator)
    chars_p = PeekableStream(chars)
    while chars_p.peek is not None:
        c = chars_p.next()
        if c in "(){},;=:":
            yield Token(c)
        elif c in " \n":
            pass
        elif c in ("'", '"'):
            yield Token("string", _scan_string(c, chars_p))
        elif c in "+-*/":
            yield Token("arithmetic", c)
        elif re.match("[.0-9]", c):
            yield Token("number", _scan(c, chars_p, "[.0-9]"))
        elif re.match("[_a-zA-Z]", c):
            yield Token("symbol", _scan(c, chars_p, "[_a-zA-Z0-9]"))
        elif c == "\t":
            raise Exception("Tab characters are not allowed in Cell")
        else:
            raise Exception("Unrecognised character: '" + c + "'.")


class Token:

    def __init__(self, typ, value=None):
        self.typ = typ
        self.value = value

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.typ == other.typ
            and self.value == other.value
        )

    def __repr__(self):
        return "Token(%s, %s)" % (repr(self.typ), repr(self.value))
