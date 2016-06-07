
from tests.util.asserts import assert_that, equals
from tests.util.test import test
# from tests.util.system_test import system_test
# from tests.util.all_examples import all_examples

from cell.lexer import lex
from cell.parser import parse, Assignment, Operation, Number

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
def Variable_assignment_gets_parsed():
    assert_that(parsed("x = 3;"), equals([Assignment("x", Number("3"))]))


# --- Example programs ---


# @system_test
# def All_examples_parse():
#     from cell.chars_in_file import chars_in_file
#     for example in all_examples():
#         with open(example, encoding="ascii") as f:
#             parsed(chars_in_file(f))
