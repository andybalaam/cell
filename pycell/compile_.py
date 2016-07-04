
# TODO: remove env if not needed

def compile_operation(expr, env):
    return "%s %s %s" % (
        compile_expr(expr[2], env),
        expr[1],
        compile_expr(expr[3], env)
    )


def compile_call(expr, env):
    return "%s()" % compile_expr(expr[1], env)


def compile_assignment(expr, env):
    # TODO: check expr[1] compiles to a symbol
    return "var %s = %s" % (
        compile_expr(expr[1], env), compile_expr(expr[2], env))


def compile_function_def(expr, env):
    # TODO: check args are symbols
    ret = "function(%s)\n{\n" % ( ", ".join(s[1] for s in expr[1]) )
    ret += compile_list(expr[2], env, 4, True)
    ret += "}\n"
    return ret


def compile_expr(expr, env):
    typ = expr[0]
    if typ == "number":
        return expr[1]
    elif typ == "string":
        return "'%s'" % expr[1].replace("'","\\'")
    elif typ == "symbol":
        return expr[1]
    elif typ == "function":
        return compile_function_def(expr, env)
    elif typ == "assignment":
        return compile_assignment(expr, env)
    elif typ == "call":
        return compile_call(expr, env)
    elif typ == "operation":
        return compile_operation(expr, env)
    else:
        raise Exception("Compiling unknown type '%s'." % str(expr))


def compile_list(exprs, env, indent=0, return_last = False):
    ret = ""
    lst_exprs = list(exprs)
    for i, expr in enumerate(lst_exprs):
        ret += " " * indent
        if return_last and i == len(lst_exprs) - 1:
            ret += "return "
        ret += compile_expr(expr, env)
        ret += ";\n"
    return ret
