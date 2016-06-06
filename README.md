# Cell Elementary Learning Language

Note: Cell is currently unfinished.  The documentation below describes the
language as it will be when it is complete.

Cell is a minimally simple programming language designed to demonstrate how to
write a programming language.

Here is an example program:

```
double =
    {:(x)
        2 * x;
    };

num1 = 3;
num2 = double( num );

answer =
    if( greater_than( num2, 5 ),
        {"LARGE!"},
        {"small."}
    );

print( answer );
```

This prints:

```
LARGE!
```

## Design Principles

Cell is designed to be as complete a programming language as possible, while
also being as small to implement as possible.

The implementation is designed to be easy to read, since the purpose is to
demonstrate how to write a programming language.

## Features

Cell has:

* Numbers (floating-point)
* Strings
* Functions

That's about it.

## Building a language

Cell provides more complex data structures using functions.  (More info
coming soon, but see Lisp's `cons` etc. for the general idea.)

## Details

* [Lexing](lexing.md)

