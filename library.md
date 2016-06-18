# The Standard Library of Cell

Cell has very simple syntax, doing as little as possible that is "special",
and doing as much as possible using functions.

For example, an `if` "statement" in Cell is not a statement at all, but is
actually a call to a function called `if`:

<!-- include "examples/libif.cell" -->
```
y = 3;
x = if( equals( y, 3 ), {"yes!";}, {"no.";} );
print( x );
```
<!-- end_include -->

This program will print "yes!", because the `if` function runs its second
argument if its first argument is true.

Before our normal program starts, Cell creates some functions and inserts them
into the global environment which is used by the [Evaluator](evaluation.md)
to look up names.  This set of names that are inserted automatically is called
the Prologue.

Some of the functions in the Prologue are normal functions written in Cell, and
some (including `if`) are "native" functions meaning that they can't be written
in Cell, so they are written in the language of the interpreter (in Cell's
case, Python).

Here is a simplified version of Cell's `if` function in Python:

    def prologue_if(env, *args):
        if args[0][1] != 0:
            to_call = args[1]
        else:
            to_call = args[2]
        call_tree = ("call", to_call, [])
        return eval_expr(call_tree)

This function checks the value of the first argument and remembers which
of the other arguments (which are functions) it is going to call.

It then creates a tree structure representing calling that function with no
arguments, and finally evaluates the function call expression it has created
and returns the result.  `eval_expr` is a function provided by the Evaluator.

We couldn't implement if in Cell directly, since we would need to be able
to say "if" in some way to be able to do it.

Another example of a native function is Cell is `set`, which goes and finds
a name in the environment where it was defined, and changes the value stored
for it.  This needs to be done natively because Cell programs can't
manipulate the environment directly.
