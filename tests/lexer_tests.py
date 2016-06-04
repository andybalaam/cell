
from tests.util.asserts import *
from tests.util.test import *

from cell.lexer import lex 

@test
def Empty_file_produces_nothing():
    assert_that( lex( "" ), equals( [] ) )

