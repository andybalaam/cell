
from tests.util.asserts import assert_that, equals, is_not, fail
from tests.util.test import test
from tests.util.system_test import system_test
from tests.util.all_examples import all_examples

from cell.lexer import (
    lex,
    LexingError,
    ArithmeticToken,
    CloseBraceToken,
    CloseBracketToken,
    ColonToken,
    CommaToken,
    EqualsToken,
    NumberToken,
    OpenBraceToken,
    OpenBracketToken,
    SemiColonToken,
    StringToken,
    SymbolToken
)

# --- Utils ---


def lexed(inp):
    return list(lex(inp))

# --- Lexing ---


@test
def Empty_file_produces_nothing():
    assert_that(lexed(""), equals([]))


@test
def Open_bracket_produces_open_bracket_token():
    assert_that(lexed("("), equals([OpenBracketToken()]))


@test
def Close_bracket_produces_close_bracket_token():
    assert_that(lexed(")"), equals([CloseBracketToken()]))


@test
def Open_brace_produces_open_brace_token():
    assert_that(lexed("{"), equals([OpenBraceToken()]))


@test
def Close_brace_produces_close_brace_token():
    assert_that(lexed("}"), equals([CloseBraceToken()]))


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


@test
def Items_separated_by_newlines_become_separate_tokens():
    assert_that(
        lexed("foo\nbar"),
        equals(
            [
                SymbolToken("foo"),
                SymbolToken("bar")
            ]
        )
    )


@test
def Symbols_may_contain_numbers_and_underscores():
    assert_that(
        lexed("foo2_bar ( "),
        equals(
            [
                SymbolToken("foo2_bar"),
                OpenBracketToken()
            ]
        )
    )


@test
def Symbols_may_start_with_underscores():
    assert_that(
        lexed("_foo2_bar ( "),
        equals(
            [
                SymbolToken("_foo2_bar"),
                OpenBracketToken()
            ]
        )
    )


@test
def Integers_are_parsed_into_number_tokens():
    assert_that(lexed("128"), equals([NumberToken("128")]))


@test
def Floating_points_are_parsed_into_number_tokens():
    assert_that(lexed("12.8"), equals([NumberToken("12.8")]))


@test
def Leading_decimal_point_produces_number_token():
    assert_that(lexed(".812"), equals([NumberToken(".812")]))


@test
def Quoted_values_produce_string_tokens():
    assert_that(lexed('"foo"'), equals([StringToken('foo')]))


@test
def Empty_quotes_produce_an_empty_string_token():
    assert_that(lexed('""'), equals([StringToken('')]))


@test
def An_unfinished_string_is_an_error():
    try:
        lexed('"foo')
        fail("Should throw")
    except LexingError as e:
        assert_that(str(e), equals("A string ran off the end of the program!"))


@test
def Commas_produce_comma_tokens():
    assert_that(lexed(","), equals([CommaToken()]))


@test
def Equals_produces_an_equals_token():
    assert_that(lexed("="), equals([EqualsToken()]))


@test
def Semicolons_produce_semicolon_tokens():
    assert_that(lexed(";"), equals([SemiColonToken()]))


@test
def Colons_produce_colon_tokens():
    assert_that(lexed(":"), equals([ColonToken()]))


@test
def Arithmetic_operators_produce_arithmetic_tokens():
    assert_that(lexed("+"), equals([ArithmeticToken("+")]))
    assert_that(lexed("-"), equals([ArithmeticToken("-")]))
    assert_that(lexed("*"), equals([ArithmeticToken("*")]))
    assert_that(lexed("/"), equals([ArithmeticToken("/")]))


@test
def Multiple_token_types_can_be_combined():
    assert_that(
        lexed('frobnicate( "Hello" + name, 4 / 5.0);'),
        equals(
            [
                SymbolToken("frobnicate"),
                OpenBracketToken(),
                StringToken("Hello"),
                ArithmeticToken("+"),
                SymbolToken("name"),
                CommaToken(),
                NumberToken("4"),
                ArithmeticToken("/"),
                NumberToken("5.0"),
                CloseBracketToken(),
                SemiColonToken()
            ]
        )
    )


@test
def A_complex_example_program_lexes():
    example = """
        double =
            {:(x)
                2 * x;
            };

        num1 = 3;
        num2 = double( num );

        answer =
            if( greater_than( num2, 5 ),
                {"LARGE!"},
                {"small."}
            );

        print( answer );
    """
    lexed(example)


@test
def Tabs_are_an_error():
    try:
        lexed("aaa\tbbb")
        fail("Should throw")
    except LexingError as e:
        assert_that(str(e), equals("Tab characters are not allowed in Cell"))


# --- Example programs ---


@system_test
def All_examples_lex():
    from cell.chars_in_file import chars_in_file
    for example in all_examples():
        with open(example, encoding="ascii") as f:
            lexed(chars_in_file(f))


# --- Details ---


@test
def Open_bracket_token_is_equal_to_open_bracket_token():
    assert_that(OpenBracketToken(), equals(OpenBracketToken()))


@test
def Open_bracket_token_is_not_equal_to_something_else():
    assert_that(OpenBracketToken(), is_not(CloseBracketToken()))
