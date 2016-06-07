import re

from cell.peekablestream import PeekableStream


def _scan(first_char, chars, allowed):
    ret = first_char
    p = chars.next
    while p is not None and re.match(allowed, p):
        ret += chars.move_next()
        p = chars.next
    return ret


def _scan_string(delim, chars):
    ret = ""
    while chars.next != delim:
        c = chars.move_next()
        if c is None:
            raise Exception("A string ran off the end of the program.")
        ret += c
    chars.move_next()
    return ret


_midsym = "[_a-zA-Z0-9]"
_stsym = "[_a-zA-Z]"

def lex(chars_iter):
    chars = PeekableStream(chars_iter)
    while chars.next is not None:
        c = chars.move_next()
        if c in " \n":              pass           # Ignore white space
        elif c in "(){},;=:":       yield (c, "")  # Special characters
        elif c in "+-*/":           yield ("operation", c)
        elif c in ("'", '"'):       yield ("string", _scan_string(c, chars))
        elif re.match("[.0-9]", c): yield ("number", _scan(c, chars, "[.0-9]"))
        elif re.match(_stsym, c):   yield ("symbol", _scan(c, chars, _midsym))
        elif c == "\t":
            raise Exception("Tab characters are not allowed in Cell.")
        else:
            raise Exception("Unrecognised character: '" + c + "'.")
