# Parsing in Cell

A parser is the part of a programming language that transforms an unstructured
stream of tokens (coming from the [lexer](lexing.md)) into tree-like structures
that reflect the expressions that are allowed in the language.


You can find Cell's parser at:
https://github.com/andybalaam/cell/blob/master/cell/parser.py
and the tests for it at:
https://github.com/andybalaam/cell/blob/master/tests/parser_tests.py

For example, if we have a program like this:

    x = 3 + 4;

which the lexer has transformed into five tokens `x`, `=`, `3`, `+` and `4`,
then the parser will transform it into something like this:

    Assign ("="):
        into x:
        the result of adding ("+"):
            3, and
            4

The indentation above is intended to demonstrate that we are building up a tree
structure.  So, if you are familiar with JSON syntax it may be helpful to
imagine the tree structure being represented as:

    {"=": [
        "x",
        { "+": [3, 4] }
    ] }

In fact, because Cell is written in Python and the tokens and parsed
expressions are both held as tuples, Cell's parser takes input like this:

    ("symbol", "x")
    ("=",)
    ("number", "3")
    ("operation", "+")
    ("number", "4")
    (";",)

(a flat list of tokens), and transforms it into a tree structure something
like this:

    ("assignment",
        ("symbol", "x"),
        ("operation",
            "+",
            ("number", "3"),
            ("number", "4")
        )
    )

Here's another example:

    print( "Hello" );

After lexing, this looks like:

    ("symbol", "print")
    ("(",)
    ("string", "Hello")
    (")",)
    (";",)

and after parsing, that becomes something like:

    ("call", ("symbol", "print"), [("string", "Hello")])

## How parsing works

The parser works through tokens one by one until it recognises what type of
expression it is dealing with.  This is not immediately clear straight away.
For example, if it sees a token `("symbol", "x")`, it could be the start of a
simple mathematical expression like `x + 3`, or it could be the start of an
assignment statement like `x = 12`.

So the parser waits until it is sure what type of expression it is dealing
with, then gathers the other parts it needs (for example if it has received
`myfunction(` as two tokens `("symbol", "myfunction")` and `("(",)`, and then it
knows this is a function call, so it reads in the list of arguments before
gathering them up and sending back a function call expression.

Because we can have nested expressions like:

    print( 3 * half_of( 14 ) );

the trees the parser sends back can have other trees nested inside them.  In
this case the parser will see `print(` and start trying to build a function
call expression, but it won't actually be able to send it back until it has
built sub-trees to represent the `half_of(` function call, and then inserted
that into the `*` expression.  Once these sub-trees have been made, the parser
can return the `print(` function call expression.

If we were writing a parser in a low-level language, we would need to use a
stack data structure to manage this nesting, but since we are using Python, we
represent it by calling functions recursively.  There is still a stack being
used underneath, but it's the stack Python itself uses to keep hold of the
chain of function calls, so we don't see it explicitly in our code.

## Cell's parsing rules

Cell programs are built up from these expression types, which are the only
types that can be returned from the parser:

* Assignment (e.g. `x = 3`)
* Operations (e.g. `4 + y`)
* Function calls (e.g. `sqrt( -1 )`)
* Function definitions (e.g. `{:(x, y) x*x + y*y;}`)

This is a smaller and simpler set of expressions than in most languages*.  The
main reason Cell needs so few expression types is because it uses functions to
provide abilities that would usually be provided by specialised expressions.

*Except Lisp.

For example, in Cell, the `if` function replaces what would normally be a
specific `if-then-else` statement or expression type.  Cell can express this as
a function because the "then" parts are passed as arguments which are actually
function definitions:

    if(
        is_even( 2 ),
        { print "Even!"; },
        { print "Odd."; }
    );

In the above code, `{ print "Even!"; }` is a tiny function with no name, that
takes no arguments, and the `if` function will call it if its first argument
evaluates to true.
