
import re

from cell.assert_implements import assert_implements
from cell.valueclass import valueclass
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
            raise LexingError("A string ran off the end of the program!")
        ret += c
    chars_p.next()
    return ret


class LexingError(Exception):
    pass


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
        if c == "(":
            yield OpenBracketToken()
        elif c == ")":
            yield CloseBracketToken()
        elif c == "{":
            yield OpenBraceToken()
        elif c == "}":
            yield CloseBraceToken()
        elif c in " \n":
            pass
        elif c in ("'", '"'):
            yield StringToken(_scan_string(c, chars_p))
        elif c == ",":
            yield CommaToken()
        elif c == ";":
            yield SemiColonToken()
        elif c == "=":
            yield EqualsToken()
        elif c == ":":
            yield ColonToken()
        elif c in "+-*/":
            yield ArithmeticToken(c)
        elif re.match("[.0-9]", c):
            yield NumberToken(_scan(c, chars_p, "[.0-9]"))
        elif re.match("[_a-zA-Z]", c):
            yield SymbolToken(_scan(c, chars_p, "[_a-zA-Z0-9]"))
        elif c == "\t":
            raise LexingError("Tab characters are not allowed in Cell")
        else:
            raise LexingError("Unrecognised character: '" + c + "'.")


@valueclass("value")
class ArithmeticToken:
    pass


@valueclass()
class CloseBraceToken:
    pass


@valueclass()
class CloseBracketToken:
    pass


@valueclass()
class ColonToken:
    pass


@valueclass()
class CommaToken:
    pass


@valueclass()
class EqualsToken:
    pass


@valueclass("value")
class NumberToken:
    pass


@valueclass()
class OpenBraceToken:
    pass


@valueclass()
class OpenBracketToken:
    pass


@valueclass()
class SemiColonToken:
    pass


@valueclass("value")
class StringToken:
    pass


@valueclass("name")
class SymbolToken:
    pass
