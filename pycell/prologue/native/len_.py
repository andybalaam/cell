
def len_(env, expr):
    if expr[0] != "string":
        raise Exception("len() can only be called for a string.")
    return ("number", len(expr[1]))
