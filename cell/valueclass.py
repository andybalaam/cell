
def valueclass(*members):
    """
    A classdecorator that makes a class into a standard value type.

    This decorator provides an __init__ method that takes in the supplied
    members and stores them in instance variables.

    This decorator also provides standard __eq__, __repr__ and __str__
    functions that use the supplied members
    """

    def _wrong_init_args_message(member_name):
        return (
            "__init__() missing 1 required positional argument: "
            + "'{arg}'").format(
                arg=member_name
        )

    def _too_many_args_message(args):
        if len(members) == 0:
            return "object() takes no parameters"
        else:
            return (
                "__init__() takes "
                + "{lenmem} positional arguments but "
                + "{lenargs} were given"
            ).format(
                lenmem=len(members) + 1,
                lenargs=len(args) + 1
            )

    def _multiple_values_message(member_name):
        return (
            "__init__() got multiple values for argument '{arg}'").format(
                arg=member_name
        )

    def value_init(self, *args, **kwargs):
        for (i, m) in enumerate(members):
            if i < len(args):
                self.__dict__[m] = args[i]
                if m in kwargs:
                    raise TypeError(_multiple_values_message(m))
            elif m in kwargs:
                self.__dict__[m] = kwargs[m]
            else:
                raise TypeError(_wrong_init_args_message(m))
        if len(args) > len(members):
            raise TypeError(_too_many_args_message(args))
        for k in kwargs:
            if k not in members:
                raise TypeError(
                    (
                        "__init__() got an unexpected keyword "
                        + "argument '{k}'"
                    ).format(k=k)
                )

    def value_eq(self, other):
        if not isinstance(other, type(self)):
            return False
        for m in members:
            if self.__dict__[m] != other.__dict__[m]:
                return False
        return True

    def value_repr(self):
        return "{type}({args})".format(
            type=type(self).__name__,
            args=", ".join(repr(self.__dict__[m]) for m in members)
        )

    def ret(cl):
        cl.__init__ = value_init
        cl.__eq__ = value_eq
        cl.__repr__ = value_repr
        return cl

    return ret
