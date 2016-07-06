
from tests.util.asserts import assert_that, assert_fails, equals
from tests.util.test import test

from pycell.lexer import lex
from pycell.parser import parse
from pycell.compile_ import compile_list
from pycell.env import Env

# --- Utils ---

def compiled(inp, env=None):
    if env is None:
        env = Env()
    return compile_list(parse(lex(inp)), env)


# --- Compiling ---

@test
def Compiling_a_number_gives_the_number():
    assert_that(
        compiled("3;"),
        equals("3;\n")
    )


@test
def Compiling_a_string_gives_the_string():
    assert_that(
        compiled("'foo';"),
        equals("'foo';\n")
    )


@test
def Compiling_a_symbol_gives_its_name():
    assert_that(
        compiled("foo;"),
        equals("foo;\n")
    )


@test
def Compiling_an_operation_gives_it():
    assert_that(
        compiled("4 + 5;"),
        equals("4 + 5;\n")
    )


@test
def Compiling_a_doublequote_string_gives_the_string():
    assert_that(
        compiled('"foo";'),
        equals("'foo';\n")
    )


@test
def Compiling_a_string_containing_a_quote_gives_it_escaped():
    assert_that(
        compiled('"\'foo";'),
        equals("'\\'foo';\n")
    )


@test
def Compiling_an_empty_function_gives_function():
    assert_that(
        compiled("{};"),
        equals("function()\n{\n}\n;\n")
    )


@test
def Compiling_a_nonempty_function_gives_function():
    assert_that(
        compiled("{3; 4;};"),
        equals("function()\n{\n    3;\n    return 4;\n}\n;\n")
    )


@test
def Compiling_a_function_with_args_gives_function():
    assert_that(
        compiled("{:(foo, bar) foo+bar;};"),
        equals("function(foo, bar)\n{\n    return foo + bar;\n}\n;\n")
    )


@test
def Compiling_an_assignment_gives_var_statement():
    assert_that(
        compiled("foo = 3;"),
        equals("var foo = 3;\n")
    )


@test
def Compiling_a_function_call_gives_a_function_call():
    assert_that(
        compiled("foo = {}; foo();"),
        equals("var foo = function()\n{\n}\n;\nfoo();\n")
    )


@test
def Compiling_a_function_call_with_args_includes_them():
    assert_that(
        compiled("foo = {:(x, y)}; foo(3, 'a');"),
        equals("var foo = function(x, y)\n{\n}\n;\nfoo(3, 'a');\n")
    )


@test
def Compiling_use_of_equals_renders_triple_equals():
    assert_that(
        compiled("equals(4, 5);"),
        equals("(4===5);\n")
    )


@test
def Compiling_use_of_if_renders_immediately_called_function():
    assert_that(
        compiled("if(1, {'true'}, {'false'});"),
        equals("""function()
{
    if( 1 !== 0 )
    {
        return 'true';
    }
    else
    {
        return 'false'
    }
}();\n""")
    )


# TODO: compiler should check e.g. symbols exist.  Share with parser?
# TODO: what about an assignment within another expression?
# TODO: similar for if etc.
# TODO: what we should really do is transform a Cell AST into a JS AST
