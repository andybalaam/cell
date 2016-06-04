
from cell.pyutil import *
from tests.util.matcher import Matcher

def assert_that( obj, matcher ):
    assert_implements( obj, object )
    assert_implements( matcher, Matcher )
    if not matcher.matches( obj ):
        raise AssertionError( matcher.description() )

def equals( expected ):
    class EqualsMatcher:
        def __init__( self, expected ):
            self.expected = expected
        def matches( self, actual ):
            self.actual = actual
            return actual == expected
        def description( self ):
            return (
                str( self.actual )
                + " does not equal "
                + str( self.expected )
                + " as expected."
            )
    return EqualsMatcher( expected )

