
from tests.util.asserts import assert_that, equals, fail
from tests.util.test import test
# from tests.util.system_test import system_test
# from tests.util.all_examples import all_examples

from cell.lexer import lex
from cell.parser import parse
from cell.eval_ import eval_
from cell.env import Env

# --- Utils ---


def evald(inp):
    return eval_(parse(lex(inp)), Env())


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


@test
def Referring_to_an_unknown_symbol_is_an_error():
    try:
        evald("x;")
        fail("Should throw")
    except Exception as e:
        assert_that(str(e), equals("Unknown symbol 'x'."))


@test
def Can_define_a_value_and_retrieve_it():
    assert_that(evald("x = 30;x;"), equals(("number", 30)))
    assert_that(evald("y = 'foo';y;"), equals(("string", "foo")))


@test
def Calling_a_function_returns_its_last_value():
    assert_that(
        evald("{10;11;}();"),
        equals(("number", 11))
    )


@test
def Body_of_a_function_can_use_arg_values():
    assert_that(
        evald("{:(x, y) x + y;}(100, 1);"),
        equals(("number", 101))
    )


@test
def Can_hold_a_reference_to_a_function_and_call_it():
    assert_that(
        evald("""
        add = {:(x, y) x + y;};
        add(20, 2.2);
        """),
        equals(("number", 22.2))
    )


@test
def A_symbol_has_different_life_inside_and_outside_a_function():
    """Define a symbol outside a function, redefine inside,
       then evaluate outside.  What happened inside the
       function should not affect the value outside."""

    assert_that(
        evald("""
            foo = "bar";
            {foo = 3;}();
            foo;
        """),
        equals(("string", "bar"))
    )


@test
def A_symbol_within_a_function_has_the_local_value():
    assert_that(
        evald("""
            foo = 3;
            bar = {foo = 77;foo;}();
            bar;
        """),
        equals(("number", 77))
    )


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
#         num2 = double( num1 );
#
#         answer =
#             if( greater_than( num2, 5 ),
#                 {"LARGE!"},
#                 {"small."}
#             );
#
#         answer;
#     """
#     assert_that(evald(example), equals(("string", "LARGE!")))


# @system_test
# def All_examples_evaluate():
#     from cell.chars_in_file import chars_in_file
#     for example in all_examples():
#         with open(example, encoding="ascii") as f:
#             parsed(chars_in_file(f))
#             TODO: check the output is correct
