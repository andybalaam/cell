
from tests.util.asserts import assert_that, equals, fail
from tests.util.test import test
from tests.util.system_test import system_test
from tests.util.all_examples import all_examples

from cell.lexer import lex

# --- Utils ---


def lexed(inp):
    return list(lex(inp))

# --- Lexing ---


@test
def Empty_file_produces_nothing():
    assert_that(lexed(""), equals([]))


@test
def Open_bracket_produces_open_bracket_token():
    assert_that(lexed("("), equals([("(", "")]))


@test
def Close_bracket_produces_close_bracket_token():
    assert_that(lexed(")"), equals([(")", "")]))


@test
def Open_brace_produces_open_brace_token():
    assert_that(lexed("{"), equals([("{", "")]))


@test
def Close_brace_produces_close_brace_token():
    assert_that(lexed("}"), equals([("}", "")]))


@test
def Multiple_brackets_become_multiple_tokens():
    assert_that(
        lexed("()"),
        equals([("(", ""), (")", "")])
    )


@test
def Single_letter_becomes_a_symbol_token():
    assert_that(lexed("a"), equals([("symbol", "a")]))


@test
def Multiple_letters_become_a_symbol_token():
    assert_that(lexed("foo"), equals([("symbol", "foo")]))


@test
def A_symbol_followed_by_a_bracket_becomes_two_tokens():
    assert_that(
        lexed("foo("),
        equals([("symbol", "foo"), ("(", "")])
    )


@test
def Items_separated_by_spaces_become_separate_tokens():
    assert_that(
        lexed("foo bar ( "),
        equals(
            [
                ("symbol", "foo"),
                ("symbol", "bar"),
                ("(", "")
            ]
        )
    )


@test
def Items_separated_by_newlines_become_separate_tokens():
    assert_that(
        lexed("foo\nbar"),
        equals(
            [
                ("symbol", "foo"),
                ("symbol", "bar")
            ]
        )
    )


@test
def Symbols_may_contain_numbers_and_underscores():
    assert_that(
        lexed("foo2_bar ( "),
        equals(
            [
                ("symbol", "foo2_bar"),
                ("(", "")
            ]
        )
    )


@test
def Symbols_may_start_with_underscores():
    assert_that(
        lexed("_foo2_bar ( "),
        equals(
            [
                ("symbol", "_foo2_bar"),
                ("(", "")
            ]
        )
    )


@test
def Integers_are_parsed_into_number_tokens():
    assert_that(lexed("128"), equals([("number", "128")]))


@test
def Floating_points_are_parsed_into_number_tokens():
    assert_that(lexed("12.8"), equals([("number", "12.8")]))


@test
def Leading_decimal_point_produces_number_token():
    assert_that(lexed(".812"), equals([("number", ".812")]))


@test
def Double_quoted_values_produce_string_tokens():
    assert_that(lexed('"foo"'), equals([("string", 'foo')]))


@test
def Single_quoted_values_produce_string_tokens():
    assert_that(lexed("'foo'"), equals([("string", 'foo')]))


@test
def Different_quote_types_allow_the_other_type_inside():
    assert_that(lexed("'f\"oo'"), equals([("string", 'f"oo')]))
    assert_that(lexed('"f\'oo"'), equals([("string", "f'oo")]))


@test
def Empty_quotes_produce_an_empty_string_token():
    assert_that(lexed('""'), equals([("string", '')]))


@test
def An_unfinished_string_is_an_error():
    try:
        lexed('"foo')
        fail("Should throw")
    except Exception as e:
        assert_that(str(e), equals("A string ran off the end of the program."))


@test
def Commas_produce_comma_tokens():
    assert_that(lexed(","), equals([(",", "")]))


@test
def Equals_produces_an_equals_token():
    assert_that(lexed("="), equals([("=", "")]))


@test
def Semicolons_produce_semicolon_tokens():
    assert_that(lexed(";"), equals([(";", "")]))


@test
def Colons_produce_colon_tokens():
    assert_that(lexed(":"), equals([(":", "")]))


@test
def Arithmetic_operators_produce_arithmetic_tokens():
    assert_that(lexed("+"), equals([("arithmetic", "+")]))
    assert_that(lexed("-"), equals([("arithmetic", "-")]))
    assert_that(lexed("*"), equals([("arithmetic", "*")]))
    assert_that(lexed("/"), equals([("arithmetic", "/")]))


@test
def Multiple_token_types_can_be_combined():
    assert_that(
        lexed('frobnicate( "Hello" + name, 4 / 5.0);'),
        equals(
            [
                ("symbol", "frobnicate"),
                ("(", ""),
                ("string", "Hello"),
                ("arithmetic", "+"),
                ("symbol", "name"),
                (",", ""),
                ("number", "4"),
                ("arithmetic", "/"),
                ("number", "5.0"),
                (")", ""),
                (";", "")
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
    except Exception as e:
        assert_that(str(e), equals("Tab characters are not allowed in Cell."))


# --- Example programs ---


@system_test
def All_examples_lex():
    from cell.chars_in_file import chars_in_file
    for example in all_examples():
        with open(example, encoding="ascii") as f:
            lexed(chars_in_file(f))
