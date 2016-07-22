
def concat(env, s1, s2):
    if s1[0] != "string" or s2[0] != "string":
        raise Exception(
            "concat() must take two strings as its arguments, not '%s, %s'." %(
                str(s1), str(s2))
        )
    return ("string", s1[1] + s2[1])

