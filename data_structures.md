# Data Structures in Cell

Even though Cell's syntax does not explicitly support data structures
(for example, there is no "[a, b, c]" style to say we want a list
containing three items), it does allow data structures through the
way you can store and retrieve values passed in to functions, and
the [library](library.md) does contain several functions for building
and working with data structures.

The most basic data structure we could want is a pair, which allows us
to hold two values together, and access either one of them.  We can make
one using the `pair` library function:

    x = pair("a", "b");

and then we can access the items stored inside using the `first` and
`second` functions:

    print(first(x));

This prints "a".

The implementation of the `pair`, `first` and `second` functions does not
use any magic - they just make use of the fact that we can return functions
from within functions, and the fact that those returned functions can
"see" the values passed in to them even after they have been returned:

<!-- include "examples/pairs.cell" -->
```
pair_ =
    {:( f, s )
        {:( which )
            if( equals( which, "f" ),
                {f;},
                {s;}
            );
        };
    };

first_ = {:(p) p("f");};

second_ = {:(p) p("s");};
```
<!-- end_include -->

`pair_` is a function that returns a function.  The returned function
takes one argument.  If that argument is "f", it returns the first
argument passed in to `pair_` (called `f`).  If not, it returns the second
(`s`).

The `first_` and `second_` functions just call the function that was returned
from `pair_`, passing in either "f" or "s" to get the argument they want.

Once you get your head around this, you understand "closures", which are
a fundamental structure in many functional programming languages, and
you have enough to be able to build up more complex data structures such
as lists and trees.
