
from pycell.lexer import lex
from pycell.parser import parse
from pycell.eval_ import eval_list

import pycell.prologue.native.char_at
import pycell.prologue.native.equals
import pycell.prologue.native.if_
import pycell.prologue.native.len_
import pycell.prologue.native.print_
import pycell.prologue.native.set_

import pycell.prologue.cell.a00_not
import pycell.prologue.cell.chars_in
import pycell.prologue.cell.pairs
import pycell.prologue.cell.lists


def import_(env):
    env.set("char_at", ("native", pycell.prologue.native.char_at.char_at))
    env.set("equals",  ("native", pycell.prologue.native.equals.equals))
    env.set("if",      ("native", pycell.prologue.native.if_.if_))
    env.set("len",     ("native", pycell.prologue.native.len_.len_))
    env.set("print",   ("native", pycell.prologue.native.print_.print_))
    env.set("set",     ("native", pycell.prologue.native.set_.set_))
    env.set("None",    ("none",))

    eval_list(parse(lex(as_text(env))), env)


def as_text(env):
    return (
        pycell.prologue.cell.a00_not.not_
        + pycell.prologue.cell.chars_in.chars_in
        + pycell.prologue.cell.pairs.pairs
        + pycell.prologue.cell.lists.lists
    )
