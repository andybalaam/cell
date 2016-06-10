
from tests.util.asserts import assert_that, equals
from tests.util.test import test
# from tests.util.system_test import system_test
# from tests.util.all_examples import all_examples

from cell.lexer import lex
from cell.parser import parse
from cell.eval_ import eval_

# --- Utils ---


def evald(inp):
    return eval_(parse(lex(inp)))

# --- Evaluating ---


@test
def Evaluating_an_empty_program_gives_none():
    assert_that(evald(""), equals(("none",)))


@test
def Evaluating_a_primitive_returns_itself():
    assert_that(evald("3;"), equals(("number", 3)))
    assert_that(evald("3.1;"), equals(("number", 3.1)))
    assert_that(evald("'foo';"), equals(("string", "foo")))


@test
def Arithmetic_expressions_come_out_correct():
    assert_that(evald("3 + 4;"), equals(("number", 7)))
    assert_that(evald("3 - 4;"), equals(("number", -1)))
    assert_that(evald("3 * 4;"), equals(("number", 12)))
    assert_that(evald("3 / 4;"), equals(("number", 0.75)))


# --- Example programs ---

# @test
# def A_complex_example_program_evaluates_correctly():
#     example = """
#         double =
#             {:(x)
#                 2 * x;
#             };
#
#         num1 = 3;
#         num2 = double( num );
#
#         answer =
#             if( greater_than( num2, 5 ),
#                 {"LARGE!"},
#                 {"small."}
#             );
#
#         print( answer );
#     """
#     parsed(example)
#
#
# @system_test
# def All_examples_evaluate():
#     from cell.chars_in_file import chars_in_file
#     for example in all_examples():
#         with open(example, encoding="ascii") as f:
#             parsed(chars_in_file(f))
#             TODO: check the output is correct
