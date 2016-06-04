
class TestFunctionType:
    def __init__( self, t ):
        self.t = t
    def __call__( self, *args ):
        return self.t( *args )

def test( t ):
    return TestFunctionType( t )

