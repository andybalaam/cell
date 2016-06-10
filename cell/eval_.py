

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
        if name in env:
            return env[name]
        else:
            raise Exception("Unknown symbol '%s'." % name)
    elif typ == "assignment":
        var_name = expr[1][1]
        env[var_name] = _single_expression(expr[2], env)
    else:
        raise Exception("Unknown expression type: " + str(expr))


def eval_(exprs, env):
    ret = ("none",)
    for expr in exprs:
        ret = _single_expression(expr, env)
    return ret
