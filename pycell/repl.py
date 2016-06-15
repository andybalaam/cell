
import pycell.library

from pycell.chars_in_file import chars_in_file
from pycell.env import Env
from pycell.eval_ import eval_iter
from pycell.lexer import lex
from pycell.parser import parse


def stringify(value):
    typ = value[0]
    if typ == "number":
        ret = str(value[1])
        if ret.endswith(".0"):
            ret = ret[:-2]
        return ret
    elif typ == "string":
        return repr(value[1])
    elif typ == "function":
        return "<function>"
    elif typ == "native":
        return "<native function>"
    elif typ == "none":
        return "None"
    else:
        raise Exception("Unknown value type '%s'" % typ)


class Prompt:

    def __init__(self, stdout):
        self.stdout = stdout
        self.values_queue = []
        stdout.write(">>> ")
        stdout.flush()

    def handle_chars(self, chars):
        for ch in chars:
            yield ch
            if ch == "\n":
                if len(self.values_queue) > 0:
                    for v in self.values_queue:
                        self.stdout.write(stringify(v))
                        self.stdout.write("\n")
                    self.stdout.write(">>> ")
                    self.values_queue.clear()
                else:
                    self.stdout.write("... ")
                self.stdout.flush()

    def value(self, value):
        self.values_queue.append(value)


def repl(stdin, stdout, stderr):
    env = Env(parent=None, stdin=stdin, stdout=stdout, stderr=stderr)
    pycell.library.import_(env)
    while True:
        try:
            p = Prompt(stdout)
            for value in eval_iter(
                    parse(lex(p.handle_chars(chars_in_file(stdin)))), env):
                p.value(value)
            break
        except Exception as e:
            stderr.write(str(e))
            stderr.write("\n")
    stdout.write("\n")
    stdout.flush()
