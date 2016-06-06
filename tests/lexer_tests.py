
from tests.util.asserts import assert_that, equals, is_not
from tests.util.test import test

from cell.lexer import lex, OpenBracketToken, CloseBracketToken, SymbolToken

# --- Utils ---


def lexed(inp):
    return list(lex(inp))

# --- Lexing ---


@test
def Empty_file_produces_nothing():
    assert_that(lexed(""), equals([]))


@test
def Open_bracket_produces_Open_bracket_token():
    assert_that(lexed("("), equals([OpenBracketToken()]))


@test
def Close_bracket_produces_Close_bracket_token():
    assert_that(lexed(")"), equals([CloseBracketToken()]))


@test
def Multiple_brackets_become_multiple_tokens():
    assert_that(
        lexed("()"),
        equals([OpenBracketToken(), CloseBracketToken()])
    )


@test
def Single_letter_becomes_a_symbol_token():
    assert_that(lexed("a"), equals([SymbolToken("a")]))


@test
def Multiple_letters_become_a_symbol_token():
    assert_that(lexed("foo"), equals([SymbolToken("foo")]))


@test
def A_symbol_followed_by_a_bracket_becomes_two_tokens():
    assert_that(
        lexed("foo("),
        equals([SymbolToken("foo"), OpenBracketToken()])
    )


@test
def Items_separated_by_spaces_become_separate_tokens():
    assert_that(
        lexed("foo bar ( "),
        equals(
            [
                SymbolToken("foo"),
                SymbolToken("bar"),
                OpenBracketToken()
            ]
        )
    )


# --- Details ---


@test
def Open_bracket_token_is_equal_to_open_bracket_token():
    assert_that(OpenBracketToken(), equals(OpenBracketToken()))


@test
def Open_bracket_token_is_not_equal_to_something_else():
    assert_that(OpenBracketToken(), is_not(CloseBracketToken()))
