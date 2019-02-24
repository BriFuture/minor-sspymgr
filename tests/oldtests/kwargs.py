
def foo( a = None, b = None, **kwargs ):
    print( a )
    print( b )
    print( kwargs )
    print( '-----foo-------')

def bar( **kwargs ):
    foo( kwargs )
    print( '-----bar-------')

foo( a = 1, b = 's' )
bar( a = 1, b = 's' )