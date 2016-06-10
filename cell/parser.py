
from cell.peekablestream import PeekableStream


class Parser:
    def __init__(self, tokens, stop_at):
        self.tokens = tokens
        self.stop_at = stop_at

    def expr(self, prev_expr):
        typ, val = self.tokens.next
        if typ in self.stop_at:
            return prev_expr
        self.tokens.move_next()
        if typ in ("number", "string", "symbol") and prev_expr is None:
            return self.expr((typ, val))
        elif typ == "operation":
            nxt = self.expr(None)
            return self.expr(("operation", val, prev_expr, nxt))
        elif typ == "(":
            args = self.args()
            return self.expr(("call", prev_expr, args))
        elif typ == "{":
            params = self.params()
            body = self.commands()
            return self.expr(("function", params, body))
        elif typ == "=":
            if prev_expr[0] != "symbol":
                raise Exception("You can't assign to anything except a symbol.")
            nxt = self.expr(None)
            return self.expr(("assignment", prev_expr, nxt))
        else:
            raise Exception("Unexpected token: " + str((typ, val)))

    def args(self):
        ret = []
        if self.tokens.next is None:
            raise Exception("An argument list ran off the end of the program.")
        typ = self.tokens.next[0]
        if typ != ")":
            arg_parser = Parser(self.tokens, ",)")
            while typ != ")":
                ret.append(arg_parser.expr(None))
                typ = arg_parser.tokens.next[0]
                arg_parser.tokens.move_next()
                if arg_parser.tokens.next is None:
                    raise Exception(
                        "An argument list ran off the end of the program.")
        else:
            self.tokens.move_next()
        return ret

    def commands(self):
        ret = []
        if self.tokens.next is None:
            raise Exception("No closing '}' for a function.")
        typ = self.tokens.next[0]
        if typ != "}":
            cmd_parser = Parser(self.tokens, ";}")
            while typ != "}":
                p = cmd_parser.expr(None)
                if p is not None:
                    ret.append(p)
                typ = cmd_parser.tokens.next[0]
                cmd_parser.tokens.move_next()
                if cmd_parser.tokens.next is None:
                    raise Exception("No closing '}' for a function.")
        else:
            self.tokens.move_next()
        return ret

    def params(self):
        ret = []
        if self.tokens.next[0] != ":":
            return ret
        self.tokens.move_next()
        typ = self.tokens.next[0]
        if typ != "(":
            raise Exception("':' must be followed by '(' in a function.")
        self.tokens.move_next()
        typ = self.tokens.next[0]
        if typ != ")":
            while typ != ")":
                ret.append(self.symbol())
                typ = self.tokens.next[0]
                self.tokens.move_next()
                if self.tokens.next is None:
                    raise Exception("No closing ')' for a parameter list")
        else:
            self.tokens.move_next()
        return ret

    def symbol(self):
        token = self.tokens.next
        if token is None:
            raise Exception("Expecting the name of symbol.")
        typ, val = token

        self.tokens.move_next()
        if typ == "symbol":
            return ("symbol", val)
        else:
            raise Exception(
                "Only symbols are allowed in function parameter lists."
                + " I found:" + str(token) + "."
            )


def parse(tokens_iterator):
    parser = Parser(PeekableStream(tokens_iterator), ";")
    while parser.tokens.next is not None:
        p = parser.expr(None)
        if p is not None:
            yield p
        parser.tokens.move_next()
