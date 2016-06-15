# Evaluation in Cell

An evaluator takes in tree structures that come from the [parser](parsing.md)
and works out what they mean.

The parser does not look up symbols to find out what is function or value you
are talking about - it just recognises known shapes and builds them into a
structure.

The evaluator is responsible for looking up names, and then actually running
the code and producing a result.  The evaluator knows that 3+7=10, and it knows
how to call functions.

You can find Cell's evaluator at:
https://github.com/andybalaam/cell/blob/master/pycell/eval_.py
and the tests for it at:
https://github.com/andybalaam/cell/blob/master/tests/eval_tests.py

For example, if we have a piece of code like this:

3 + 4;

which has been parsed into a tree like this:


    ("operation",
        "+",
        ("number", "3"),
        ("number", "4")
    )

then the evaluator will do the calculation, and return a value like this:

   ("number", 7)

Notice that the `7` is no longer in quotes - the evaluator first evaluated the
two tree nodes and converted them from unprocessed text ("3" and "4") into
real numeric values, before adding them up and returning the numeric value 7.

The evaluator keeps hold of the names of things, and it must make sure names
can only be seen from the right place.

For example:

    x = "World!";
    myfn = {
        x = "Hello, ";
        print( x );
    };
    myfn();
    print( x );

should print "Hello, " and then "World!".  If the evaluator messes up the
scoping rules, it will print "Hello, " twice, because the changed value of `x`
will leak out.

Note: in some programming languages some leaking like this is allowed and
expected, but in Cell there is no leakage.

More complicated than that is the idea of closures, where the scope of a
function can follow it around, so that this program:

    outerfn = {
        x = 12;
        innerfn = {
            print(x);
        };
        innerfn;
    };

    thing = outerfn();
    thing();

should print "12", because the `x` defined inside `outerfn` has been carried
around with `innerfn`.  Here, `outerfn` is a function that returns another
function from inside it (`innerfn`).

The second-last line of the program calls `outerfn` and stores the result
(which is `innerfn`) inside a new name called `thing`.  So now `thing` refers
to `innerfn`.  So when we call `thing` on the last line of the program, we are
calling `innerfn`, and `innerfn` can still see `x` with a value of 12.

This gets much more complicated when values can change, since every time we
call `outerfn` we get back a new closure, and each could have its own version
of `x`.  In fact, we can use this mechanism to build up something like
object-oriented programs with objects (functions, here) than can hold state
inside them.

[Changing values is done in the `set` native function, which is described on
the [Library](library.md) page.]

To handle all the names, Cell creates an "Environment" for each function, which
holds all the names defined in that function (and the values they point to,
such as the number 3, a string, or another function).  Each environment also
points "out" to another environment representing the scope within which it was
defined.  At the top is the global scope, which is where names that are
assigned outside of all functions go.  The global scope environment does not
point to any scope further "out".

So an environment is really just a name-value mapping, and an optional pointer
to another environment.  In a language like Python where garbage collection
is done for us, its implementation is quite simple.  You can find Cell's
environment implementation here:
https://github.com/andybalaam/cell/blob/master/pycell/env.py

The evaluator understands assignments such as `x = 3;` or
`myfn={print("foo");};` to mean it should insert a new name/value pair into the
current environment.

Then when we refer to a name as in `x * 2;` or `myfn();` the evaluator looks
up the name in the current environment, and keeps looking into further out
environments until it find the name, and replaces that part of the tree with
the value it has found for that name.

The evaluator continues to replace parts of the tree with values it has looked
up, and to combine those values together with rules it knows (such as `+`)
until there is just one value left, which is returned somewhere, or thrown away
(presumably after some side-effect like printing has happened).

In order to do useful thing like printing, and in Cell's case, even basic
things like `if` or `for`, as well as changing values using `set`, we need some
functions.  These are defined in the [Library](library.md).

