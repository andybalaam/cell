
from tests.util.asserts import assert_that, equals, fail
from tests.util.test import test
# from tests.util.system_test import system_test
# from tests.util.all_examples import all_examples

from cell.lexer import lex
from cell.parser import parse, Assignment, Operation, Number, Symbol

# --- Utils ---


def parsed(inp):
    return list(parse(lex(inp)))

# --- Parsing ---


@test
def Empty_file_produces_nothing():
    assert_that(parsed(""), equals([]))


@test
def Number_is_parsed_as_expression():
    assert_that(parsed("56;"), equals([Number("56")]))


@test
def Sum_of_numbers_is_parsed_as_expression():
    assert_that(
        parsed("32 + 44;"),
        equals(
            [
                Operation("+", Number("32"), Number("44"))
            ]
        )
    )


@test
def Difference_of_symbol_and_number_is_parsed_as_expression():
    assert_that(
        parsed("foo - 44;"),
        equals(
            [
                Operation("-", Symbol("foo"), Number("44"))
            ]
        )
    )


@test
def Multiplication_of_symbols_is_parsed_as_expression():
    assert_that(
        parsed("foo * bar;"),
        equals(
            [
                Operation("*", Symbol("foo"), Symbol("bar"))
            ]
        )
    )


@test
def Variable_assignment_gets_parsed():
    assert_that(
        parsed("x = 3;"),
        equals(
            [
                Assignment(Symbol("x"), Number("3"))
            ]
        )
    )


@test
def Assigning_to_a_number_is_an_error():
    try:
        parsed("3 = x;")
        fail("Should throw")
    except Exception as e:
        assert_that(
            str(e),
            equals("Unexpected token after a number: ('=', '')")
        )


# --- Example programs ---


# @system_test
# def All_examples_parse():
#     from cell.chars_in_file import chars_in_file
#     for example in all_examples():
#         with open(example, encoding="ascii") as f:
#             parsed(chars_in_file(f))
