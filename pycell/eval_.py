import inspect

from pycell.env import Env


def _operation(expr, env):
    arg1 = eval_expr(expr[2], env)
    arg2 = eval_expr(expr[3], env)
    if expr[1] == "+":
        return ("number", arg1[1] + arg2[1])
    elif expr[1] == "-":
        return ("number", arg1[1] - arg2[1])
    elif expr[1] == "*":
        return ("number", arg1[1] * arg2[1])
    elif expr[1] == "/":
        return ("number", arg1[1] / arg2[1])
    else:
        raise Exception("Unknown operation: " + expr[1])


def fail_if_wrong_number_of_args(params, args):
    if len(params) != len(args):
        raise Exception((
            "%d arguments passed to function, but it "
            + "requires %d arguments."
        ) % (len(args), len(params)))


def _function_call(expr, env):
    fn = eval_expr(expr[1], env)
    args = list((eval_expr(a, env) for a in expr[2]))
    if fn[0] == "function":
        params = fn[1]
        fail_if_wrong_number_of_args(params, args)
        body = fn[2]
        new_env = fn[3]
        for p, a in zip(params, args):
            new_env.set(p[1], a)
        return eval_list(body, new_env)
    elif fn[0] == "native":
        py_fn = fn[1]
        params = inspect.getargspec(py_fn).args
        fail_if_wrong_number_of_args(params[1:], args)
        return fn[1](env, *args)
    else:
        raise Exception(
            "Attempted to call something that is not a function: %s" %
            str(fn)
        )


def eval_expr(expr, env):
    typ = expr[0]
    if typ == "number":
        return ("number", float(expr[1]))
    elif typ == "string":
        return ("string", expr[1])
    elif typ == "none":
        return ("none",)
    elif typ == "operation":
        return _operation(expr, env)
    elif typ == "symbol":
        name = expr[1]
        ret = env.get(name)
        if ret is None:
            raise Exception("Unknown symbol '%s'." % name)
        else:
            return ret
    elif typ == "assignment":
        var_name = expr[1][1]
        val = eval_expr(expr[2], env)
        env.set(var_name, val)
        return val
    elif typ == "call":
        return _function_call(expr, env)
    elif typ == "function":
        return ("function", expr[1], expr[2], Env(env))
    else:
        raise Exception("Unknown expression type: " + str(expr))


def eval_iter(exprs, env):
    for expr in exprs:
        yield eval_expr(expr, env)


def eval_list(exprs, env):
    ret = ("none",)
    for expr in eval_iter(exprs, env):
        ret = expr
    return ret
