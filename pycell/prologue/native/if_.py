
from pycell.eval_ import eval_expr

def if_(env, t, then_fn, else_fn):
    if t[0] != "number":
        raise Exception(
            "Only numbers may be passed to an if, but I was passed '%s'"
            % t
        )
    to_call = then_fn if t[1] != 0 else else_fn
    return eval_expr(("call", to_call, []), env)
