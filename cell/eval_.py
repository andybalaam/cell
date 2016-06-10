

def _operation(expr):
    arg1 = _single_expression(expr[2])
    arg2 = _single_expression(expr[3])
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


def _single_expression(expr):
    if expr[0] == "number":
        return ("number", float(expr[1]))
    elif expr[0] == "string":
        return ("string", expr[1])
    elif expr[0] == "operation":
        return _operation(expr)
    else:
        raise Exception("Unknown expression type: " + str(expr))


def eval_(exprs):
    ret = ("none",)
    for expr in exprs:
        ret = _single_expression(expr)
    return ret
