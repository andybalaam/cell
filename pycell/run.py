from pycell.chars_in_file import chars_in_file
from pycell.env import Env
from pycell.eval_ import eval_list
from pycell.lexer import lex
from pycell.parser import parse


def run(argv, stdin, stdout, stderr):
    env = Env(stdin, stdout, stderr)
    with open(argv[1]) as f:
        eval_list(parse(lex(chars_in_file(f))), env)
