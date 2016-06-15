
import pycell.prologue.native.if_
import pycell.prologue.native.equals
import pycell.prologue.native.print_


def import_(env):
    env.set("if",     ("native", pycell.prologue.native.if_.if_))
    env.set("equals", ("native", pycell.prologue.native.equals.equals))
    env.set("print",  ("native", pycell.prologue.native.print_.print_))
    env.set("None",   ("none",))
