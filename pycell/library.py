
from pycell.lexer import lex
from pycell.parser import parse
from pycell.eval_ import eval_list

import pycell.prologue.native.if_
import pycell.prologue.native.equals
import pycell.prologue.native.print_
import pycell.prologue.native.set_

import pycell.prologue.cell.pairs


def import_(env):
    env.set("if",     ("native", pycell.prologue.native.if_.if_))
    env.set("equals", ("native", pycell.prologue.native.equals.equals))
    env.set("print",  ("native", pycell.prologue.native.print_.print_))
    env.set("set",    ("native", pycell.prologue.native.set_.set_))
    env.set("None",   ("none",))

    eval_list(parse(lex(pycell.prologue.cell.pairs.pairs)), env)
