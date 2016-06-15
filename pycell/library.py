
import pycell.prologue.native.if_
import pycell.prologue.native.equals

def import_(env):
    env.set("if",     ("native", pycell.prologue.native.if_.if_))
    env.set("equals", ("native", pycell.prologue.native.equals.equals))
