from cell.env import Env


def _operation(expr, env):
    arg1 = _single_expression(expr[2], env)
    arg2 = _single_expression(expr[3], env)
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


def _function_call(expr, env):
    fn = expr[1]
    args = expr[2]
    params = fn[1]
    body = fn[2]
    new_env = Env(env)
    for p, a in zip(params, args):
        new_env.set(p[1], _single_expression(a, env))
    return eval_(body, new_env)


def _single_expression(expr, env):
    typ = expr[0]
    if typ == "number":
        return ("number", float(expr[1]))
    elif typ == "string":
        return ("string", expr[1])
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
        env.set(var_name, _single_expression(expr[2], env))
    elif typ == "call":
        return _function_call(expr, env)
    elif typ == "function":
        pass
    else:
        raise Exception("Unknown expression type: " + str(expr))


def eval_(exprs, env):
    ret = ("none",)
    for expr in exprs:
        ret = _single_expression(expr, env)
    return ret
