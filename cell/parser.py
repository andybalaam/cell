
from cell.valueclass import valueclass


def _parse(first_token, tokens):
    typ, val = first_token
    if typ == "symbol":      # expression or assignment
        second_token = next(tokens)
        return Assignment(val, _parse(next(tokens), tokens))
    elif typ == "number":
        typ2, val2 = next(tokens)
        if typ2 == ";":
            return Number(val)
        elif typ2 == "operation":
            return Operation(val2, Number(val), _parse(next(tokens), tokens))
    else:
        raise Exception("Unknown token type " + str(first_token))


def parse(tokens):
    for i in tokens:
        yield _parse(i, tokens)


@valueclass("name", "value")
class Assignment:
    pass


@valueclass("value")
class Number:
    pass


@valueclass("operator", "value1", "value2")
class Operation:
    pass
