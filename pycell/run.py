import pycell.library

from pycell.chars_in_file import chars_in_file
from pycell.env import Env
from pycell.eval_ import eval_list
from pycell.lexer import lex
from pycell.parser import parse


def run(filename, stdin, stdout, stderr):
    env = Env(stdin=stdin, stdout=stdout, stderr=stdout)
    pycell.library.import_(env)
    with open(filename, encoding="ascii") as f:
        eval_list(parse(lex(chars_in_file(f))), env)
