
from io import StringIO

import pycell.library

from pycell.env import Env
from pycell.eval_ import eval_list
from pycell.lexer import lex
from pycell.parser import parse

from tests.util.asserts import assert_that, equals
from tests.util.test import test
from tests.util.system_test import system_test
from tests.util.all_examples import all_examples

# --- Utils


def runned(inp):
    with StringIO() as stdin, StringIO() as stdout:
        env = Env(stdin=stdin, stdout=stdout, stderr=stdout)
        pycell.library.import_(env)
        return eval_list(parse(lex(inp)), env)

# --- Tests


@test
def A_complex_example_program_evaluates_correctly():
    example = """
        double =
            {:(x)
                2 * x;
            };

        num1 = 3;
        num2 = double( num1 );

        answer =
            if( equals( num2, 6 ),
                {"LARGE!"},
                {"small."}
            );

        answer;
    """
    assert_that(runned(example), equals(("string", "LARGE!")))


@system_test
def All_examples_evaluate():
    from pycell.run import run
    for example in all_examples():
        with StringIO() as stdin, StringIO() as stdout:
            run(["", example], stdin, stdout, stdout)
            with open(example[:-5] + ".output.txt") as outputfile:
                assert_that(stdout.getvalue(), equals(outputfile.read()))
