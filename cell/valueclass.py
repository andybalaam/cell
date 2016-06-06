
def valueclass(*members):
    """
    A classdecorator that makes a class into a standard value type.

    This decorator provides an __init__ method that takes in the supplied
    members and stores them in instance variables.

    This decorator also provides standard __eq__, __repr__ and __str__
    functions that use the supplied members
    """

    def ret(cl):
        def token_eq(self, other):
            if not isinstance(other, type(self)):
                return False
            for m in members:
                if self.__dict__[m] != other.__dict__[m]:
                    return False
            return True

        def token_repr(self):
            return "{type}({args})".format(
                type=type(self).__name__,
                args=", ".join(repr(self.__dict__[m]) for m in members)
            )

        cl.__eq__ = token_eq
        cl.__repr__ = token_repr
        return cl

    return ret
