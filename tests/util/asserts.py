
from pycell.assert_implements import assert_implements
from tests.util.matcher import Matcher

# Inspired by Hamcrest


def assert_that(obj, matcher):
    assert_implements(obj, object)
    assert_implements(matcher, Matcher)
    if not matcher.matches(obj):
        raise AssertionError(matcher.description())


def assert_fails(error, fn, *args):
    try:
        fn(*args)
        fail("Should throw")
    except Exception as e:
        assert_that(str(e), equals(error))


def equals(expected):
    class EqualsMatcher:

        def __init__(self, expected):
            self.expected = expected

        def matches(self, actual):
            self.actual = actual
            return actual == expected

        def description(self):
            ret = (
                repr(self.actual)
                + " does not equal "
                + repr(self.expected)
                + " as expected."
            )
            if len(ret) > 80:
                ret = """Values are not equal (actual then expected):
%s
%s
""" % ( repr(self.actual), repr(self.expected))
            return ret
    return EqualsMatcher(expected)


def is_not(expected):
    class NotEqualsMatcher:

        def __init__(self, expected):
            self.expected = expected

        def matches(self, actual):
            self.actual = actual
            return actual != expected

        def description(self):
            return (
                str(self.actual)
                + " equals "
                + str(self.expected)
                + " but we expected it not to."
            )
    return NotEqualsMatcher(expected)


def fail(msg):
    raise AssertionError(msg)
