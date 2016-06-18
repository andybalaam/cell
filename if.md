# The if Function

Using an if-then-else structure in Cell works differently from in other
languages, because in Cell, `if` is a function, not a special construct.

The `if` function takes in 3 arguments: a test, and two functions.  The first
function will be called if the test is true, and the second will be called if
the test is false.

The test must be a number, and if it's zero, Cell considers it false.
Otherwise, Cell considers it true.

Here is an example:

<!-- include "examples/two_ifs.cell" -->
```
flower = "rose";

if ( equals( flower, "rose" ),
    {
        print( "The flower is a rose." );
    },
    {
        print( "No roses today." );
    }
);

if ( equals( flower, "violet" ),
    {
        print( "Violets!!!!" );
    },
    {
        print( "No violets." );
    }
);
```
<!-- end_include -->

When we run this program, it prints this:

<!-- include "examples/two_ifs.output.txt" -->
```
The flower is a rose.
No violets.
```
<!-- end_include -->

The parts that start and end with `{` and `}` are actually functions that take
no arguments.  The `if` function calls one or other of them, depending on the
result of the test passed in as its first argument.

Above, the tests that were passed in were `equals( flower, "rose" )` and
`equals( flower, "violet" )`.  The equals function returns a true value if its
two arguments are the same, and a false value otherwise.

You can find out more about defining and using functions on the
[Syntax](syntax.md) page.
