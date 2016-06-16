
def _do_set(env, name, value):
    if env.contains(name):
        env.set(name, value)
    elif env.parent is not None:
        _do_set(env.parent, name, value)
    else:
        raise Exception(
            "Attempted to set name '%s' but it does not exist." %
            name
        )

def set_(env, symbol_name, value):
    if symbol_name[0] != "string":
        raise Exception(
            "set() takes a string as its first argument, but was: %s" %
            str(symbol_name)
        )
    _do_set(env, symbol_name[1], value)
    return value
