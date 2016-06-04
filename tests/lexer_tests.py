
from tests.util.asserts import *
from tests.util.test import *

from cell.lexer import *

# --- Utils ---

def lexed( inp ):
    return list( lex( inp ) )

# --- Lexing ---

@test
def Empty_file_produces_nothing():
    assert_that( lexed( "" ), equals( [] ) )


@test
def Open_bracket_produces_Open_bracket_token():
    assert_that( lexed( "(" ), equals( [OpenBracketToken()] ) )


@test
def Close_bracket_produces_Close_bracket_token():
    assert_that( lexed( ")" ), equals( [CloseBracketToken()] ) )


@test
def Multiple_brackets_become_multiple_tokens():
    assert_that(
        lexed( "()" ),
        equals( [OpenBracketToken(), CloseBracketToken()] )
    )



# --- Details ---

@test
def Open_bracket_token_is_equal_to_open_bracket_token():
    assert_that( OpenBracketToken(), equals( OpenBracketToken() ) )


@test
def Open_bracket_token_is_not_equal_to_something_else():
    assert_that( OpenBracketToken(), is_not( CloseBracketToken() ) )

