
from cell.pyutil import *
from cell.iterable import Iterable

def lex( chars ):
    assert_implements( chars, Iterable )
    for c in chars:
        if c == "(":
            yield OpenBracketToken()
        elif c == ")":
            yield CloseBracketToken()

def token( cl ):
    def token_eq( self, other ):
        return type( other ) == type( self )
    cl.__eq__ = token_eq
    return cl

@token
class OpenBracketToken:
    pass

@token
class CloseBracketToken:
    pass

