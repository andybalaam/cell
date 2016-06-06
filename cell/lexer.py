
from cell.assert_implements import assert_implements
from cell.valueclass import valueclass
from cell.iterable import Iterable


def _is_letter(c):
    return True


def _symbol(first_char, chars_iter):
    ret = first_char
    for c in chars_iter:
        if not _is_letter(c):
            break
        ret += c
    return SymbolToken(ret)


class LexingError(Exception):
    pass


def lex(chars):
    assert_implements(chars, Iterable)
    chars_iter = chars.__iter__()
    for c in chars_iter:
        if c == "(":
            yield OpenBracketToken()
        elif c == ")":
            yield CloseBracketToken()
        elif _is_letter(c):
            yield _symbol(c, chars_iter)
        else:
            raise LexingError("Unrecognised character: '" + c + "'.")


@valueclass("name")
class SymbolToken:

    def __init__(self, name):
        self.name = name


@valueclass()
class OpenBracketToken:
    pass


@valueclass()
class CloseBracketToken:
    pass
