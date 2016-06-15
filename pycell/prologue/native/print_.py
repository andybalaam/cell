
def _strvalue(value):
    typ = value[0]
    if typ == "number":
        ret = str(value[1])
        if ret.endswith(".0"):
            ret = ret[:-2]
        return ret
    elif typ == "string":
        return value[1]
    elif typ == "function":
        return "<function>"
    elif typ == "native":
        return "<native function>"
    else:
        raise Exception("Unknown value type '%s'" % typ)


def print_(env, value):
    env.stdout.write("%s\n" % _strvalue(value))
    return ("none",)
