
from tests.util.asserts import assert_that, equals, fail
from tests.util.test import test
from tests.util.system_test import system_test
from tests.util.all_examples import all_examples

from cell.lexer import lex
from cell.parser import parse

# --- Utils ---


def parsed(inp):
    return list(parse(lex(inp)))

# --- Parsing ---


@test
def Empty_file_produces_nothing():
    assert_that(parsed(""), equals([]))


# --- Example programs ---


@system_test
def All_examples_parse():
    from cell.chars_in_file import chars_in_file
    for example in all_examples():
        with open(example, encoding="ascii") as f:
            parsed(chars_in_file(f))
