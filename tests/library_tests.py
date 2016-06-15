
from tests.util.asserts import assert_that, assert_fails, equals, fail
from tests.util.test import test

from pycell.env import Env
from pycell.eval_ import eval_list
from pycell.lexer import lex
from pycell.parser import parse
from pycell.prologue.native.if_ import if_

import pycell.library

# --- Utils


def evald(inp):
    env = Env()
    pycell.library.import_(env)
    return eval_list(parse(lex(inp)), env)


# --- Tests


@test
def if_calls_then_if_first_argument_is_nonzero():
    assert_that(
        evald('if( 1, {"t";}, {"f";} );'),
        equals(evald('"t";'))
    )


@test
def if_calls_else_if_first_argument_is_zero():
    assert_that(
        evald('if( 0, {"t";}, {"f";} );'),
        equals(evald('"f";'))
    )


@test
def Call_if_with_a_nonnumber_is_an_error():
    assert_fails(
        "Only numbers may be passed to an if, but I was passed "
            + "'('string', 'x')'",
        evald,
        'if("x", {}, {});'
    )
