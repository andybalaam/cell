
import re

from cell.assert_implements import assert_implements
from cell.valueclass import valueclass
from cell.iterable import Iterable


_number_or_decimal_point_re = re.compile("[.0-9]")


def _is_number_or_decimal_point(c):
    return c is not None and _number_or_decimal_point_re.match(c)


_letter_re = re.compile("[a-zA-Z]")


def _is_letter(c):
    return c is not None and _letter_re.match(c)

_letter_number_underscore_re = re.compile("[_a-zA-Z0-9]")


def _is_letter_number_or_underscore(c):
    return c is not None and _letter_number_underscore_re.match(c)


def _symbol(first_char, chars_p):
    assert type(chars_p) is PeekableStream
    ret = first_char
    while _is_letter_number_or_underscore(chars_p.peek()):
        c = chars_p.next()
        ret += c
    return SymbolToken(ret)


def _number(first_char, chars_p):
    assert type(chars_p) is PeekableStream
    ret = first_char
    while _is_number_or_decimal_point(chars_p.peek()):
        c = chars_p.next()
        ret += c
    return NumberToken(ret)


class LexingError(Exception):
    pass


class PeekableStream:
    """
    Turns an iterator into something we can peek ahead one item of.
    """

    def __init__(self, iterable):
        assert_implements(iterable, Iterable)
        self.iterable = iterable.__iter__()
        self._fill()

    def _fill(self):
        try:
            self._next = self.iterable.__next__()
        except StopIteration:
            self._next = None

    def peek(self):
        return self._next

    def stopped(self):
        return self.peek() is None

    def next(self):
        ret = self.peek()
        self._fill()
        return ret


def lex(chars):
    assert_implements(chars, Iterable)
    chars_p = PeekableStream(chars)
    while not chars_p.stopped():
        c = chars_p.next()
        if c == "(":
            yield OpenBracketToken()
        elif c == ")":
            yield CloseBracketToken()
        elif c == " ":
            pass
        elif _is_number_or_decimal_point(c):
            yield _number(c, chars_p)
        elif _is_letter(c):
            yield _symbol(c, chars_p)
        else:
            raise LexingError("Unrecognised character: '" + c + "'.")


@valueclass("name")
class SymbolToken:
    pass


@valueclass("value")
class NumberToken:
    pass


@valueclass()
class OpenBracketToken:
    pass


@valueclass()
class CloseBracketToken:
    pass
