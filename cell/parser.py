
from cell.peekablestream import PeekableStream


class Parser:
    def __init__(self, tokens, stop_at):
        self.tokens = tokens
        self.stop_at = stop_at

    def next_expression(self, prev):
        typ, value = self.tokens.next
        if typ in self.stop_at:
            return prev
        self.tokens.move_next()
        if typ in ("number", "string", "symbol") and prev is None:
            return self.next_expression((typ, value))
        elif typ == "operation":
            nxt = self.next_expression(None)
            return self.next_expression(("operation", value, prev, nxt))
        elif typ == "(":
            args = self.multiple(",", ")")
            return self.next_expression(("call", prev, args))
        elif typ == "{":
            params = self.params()
            body = self.multiple(";", "}")
            return self.next_expression(("function", params, body))
        elif typ == "=":
            if prev[0] != "symbol":
                raise Exception("You can't assign to anything except a symbol.")
            nxt = self.next_expression(None)
            return self.next_expression(("assignment", prev, nxt))
        else:
            raise Exception("Unexpected token: " + str((typ, value)))

    def params(self):
        if self.tokens.next[0] != ":":
            return []
        self.tokens.move_next()
        typ = self.tokens.next[0]
        if typ != "(":
            raise Exception("':' must be followed by '(' in a function.")
        self.tokens.move_next()
        ret = self.multiple(",", ")")
        for param in ret:
            if param[0] != "symbol":
                raise Exception(
                    "Only symbols are allowed in function parameter lists."
                    + " I found: " + str(param) + "."
                )
        return ret

    def multiple(self, sep, end):
        ret = []
        self.fail_if_at_end(end)
        typ = self.tokens.next[0]
        if typ == end:
            self.tokens.move_next()
        else:
            arg_parser = Parser(self.tokens, (sep, end))
            while typ != end:
                p = arg_parser.next_expression(None)
                if p is not None:
                    ret.append(p)
                typ = self.tokens.next[0]
                self.tokens.move_next()
                self.fail_if_at_end(end)
        return ret

    def fail_if_at_end(self, expected):
        if self.tokens.next is None:
            raise Exception("Hit end of file - expected '%s'." % expected)


def parse(tokens_iterator):
    parser = Parser(PeekableStream(tokens_iterator), ";")
    while parser.tokens.next is not None:
        p = parser.next_expression(None)
        if p is not None:
            yield p
        parser.tokens.move_next()
