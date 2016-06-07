
from cell.valueclass import valueclass


def _parse(first_token, tokens):
    typ1, val1 = first_token
    if typ1 == "symbol":      # expression or assignment
        expr1 = Symbol(val1)
        typ2, val2 = next(tokens)
        if typ2 == "=":
            return Assignment(expr1, _parse(next(tokens), tokens))
        elif typ2 == "operation":
            return Operation(val2, expr1, _parse(next(tokens), tokens))
        elif typ2 == ";":
            return expr1
        else:
            raise Exception(
                "Unexpected token after a symbol:" + str((typ2, val2)))

    elif typ1 == "number":
        expr1 = Number(val1)
        typ2, val2 = next(tokens)
        if typ2 == ";":
            return expr1
        elif typ2 == "operation":
            return Operation(val2, expr1, _parse(next(tokens), tokens))
        else:
            raise Exception(
                "Unexpected token after a number: " + str((typ2, val2)))
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


@valueclass("value")
class Symbol:
    pass
