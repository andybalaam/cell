
from tests.util.asserts import assert_that, equals, fail
from tests.util.test import test
# from tests.util.system_test import system_test
# from tests.util.all_examples import all_examples

from cell.lexer import lex
from cell.parser import parse
from cell.eval_ import eval_
from cell.env import Env

# --- Utils ---


def evald(inp, env=None):
    if env is None:
        env = Env()
    return eval_(parse(lex(inp)), env)


def assert_fails(program, error, env=None):
    try:
        evald(program, env)
        fail("Should throw")
    except Exception as e:
        assert_that(str(e), equals(error))


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
    assert_fails("x;", "Unknown symbol 'x'.")


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


@test
def Native_function_gets_called():
    def native_fn(env, x, y):
        return ("number", x[1] + y[1])
    env = Env()
    env.set("native_fn", ("native", native_fn))
    assert_that(evald("native_fn( 2, 8 );", env), equals(("number", 10)))


@test
def Wrong_number_of_arguments_to_a_function_is_an_error():
    assert_fails(
        "{}(3);",
        "1 arguments passed to function, but it requires 0 arguments."
    )
    assert_fails(
        "x={:(a, b, c)}; x(3, 2);",
        "2 arguments passed to function, but it requires 3 arguments."
    )


@test
def Wrong_number_of_arguments_to_a_native_function_is_an_error():
    def native_fn0(env):
        return ("number", 12)
    def native_fn3(env, x, y, z):
        return ("number", 12)
    env = Env()
    env.set("native_fn0", ("native", native_fn0))
    env.set("native_fn3", ("native", native_fn3))
    assert_fails(
        "native_fn0(3);",
        "1 arguments passed to function, but it requires 0 arguments.",
        env
    )
    assert_fails(
        "native_fn3(3, 2);",
        "2 arguments passed to function, but it requires 3 arguments.",
        env
    )


@test
def A_native_function_can_edit_the_environment():
    def mx3(env):
        env.set("x", ("number", 3))
    env = Env()
    env.set("make_x_three", ("native", mx3))
    assert_that(
        evald("x=1;make_x_three();x;", env),
        equals(("number", 3))
    )


# A_closure_holds_updateable_values


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
