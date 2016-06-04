
from cell.pyutil import *
from cell.iterable import Iterable

def lex( chars ):
    assert_implements( chars, Iterable )
    for c in chars:
        if c == "(":
            yield OpenBracketToken()
        elif c == ")":
            yield CloseBracketToken()


class OpenBracketToken:
    def __eq__( self, other ):
        return type( other ) == OpenBracketToken

class CloseBracketToken:
    def __eq__( self, other ):
        return type( other ) == CloseBracketToken


