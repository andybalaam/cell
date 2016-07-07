
# TODO: remove env if not needed

def compile_operation(expr, env):
    return "%s %s %s" % (
        compile_expr(expr[2], env),
        expr[1],
        compile_expr(expr[3], env)
    )


def native_equals(args, env):
    if len(args) != 2:
        raise Exception(
            "Wrong number of argumentss to equals - expected 2, but got %d"
                % len(args)
        )
    else:
        return "(%s===%s ? 1 : 0)" % tuple(compile_expr(e, env) for e in args)


def native_if(args, env):
    if len(args) != 3:
        raise Exception(
            "Wrong number of arguments to equals - expected 3, but got %d"
                % len(args)
        )
    else:
        return (
            """(function() {
    if( %s !== 0 ) {
%s    } else {
%s    }
})()""" % (
            compile_expr(args[0], env),
            compile_list(args[1][2], env, 8, True),
            compile_list(args[2][2], env, 8, True)
        )
    )


def native_print(args, env):
    if len(args) != 1:
        raise Exception(
            "Wrong number of arguments to equals - expected 1, but got %d"
                % len(args)
        )
    else:
        return (
            "console.log(%s)" % (
                ", ".join(compile_expr(e, env) for e in args)
            )
        )


def native_set(args, env):
    if len(args) != 2:
        raise Exception(
            "Wrong number of arguments to set - expected 2, but got %d"
                % len(args)
        )
    else:
        # TODO: check args[1] compiles to a string, which refers
        #       to the name of an existing symbol
        var_name = compile_expr(args[0], env)
        if var_name[0] == "'":
            return (
                "(%s = %s)" % ( var_name[1:-1], compile_expr(args[1], env) )
            )
        else:
            # TODO: use eval to set the variable
            return "TODO"


def compile_call(expr, env):
    fn_name = compile_expr(expr[1], env)
    if fn_name == "equals":
        return native_equals(expr[2], env)
    elif fn_name == "if":
        return native_if(expr[2], env)
    elif fn_name == "print":
        return native_print(expr[2], env)
    elif fn_name == "set":
        return native_set(expr[2], env)
    else:
        return (
            "%s(%s)" % (
                fn_name,
                ", ".join(compile_expr(e, env) for e in expr[2])
            )
        )


def compile_assignment(expr, env):
    # TODO: check expr[1] compiles to a symbol
    # TODO: add symbol value to environment and check it later
    return "var %s = %s" % (
        compile_expr(expr[1], env), compile_expr(expr[2], env))


def compile_function_def(expr, env):
    # TODO: check args are symbols
    ret = "(function(%s) {\n" % ( ", ".join(s[1] for s in expr[1]) )
    ret += compile_list(expr[2], env, 4, True)
    ret += "})\n"
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
