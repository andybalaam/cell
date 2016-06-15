# Cell Elementary Learning Language

Cell is a minimally simple programming language designed to demonstrate how to
write a programming language.

Here is an example program:

<!-- include "examples/example1.cell" -->
```
square = {:(x) x * x;};

num1 = 3;
num2 = square( num1 );

if( equals( num1, num2 ),
    {
        print( "num1 equals num2." );
    },
    {
        print( "num1 does not equal num2." );
    }
);
```
<!-- end_include -->

This prints:

<!-- include "examples/example1.output.txt" -->
```
num1 does not equal num2.
```
<!-- end_include -->

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

## Interacting with Cell

Cell has an interactive environment which can be launched by running the Cell
program with no arguments:

<!-- include "examples/www.cellsession" -->
```
>>> 137 + 349;
486
>>> 5/10;
0.5
>>> 21 + 35 + 12 + 7;
75
>>> if(equals(0, 1), {"illogical";}, {"logical";});
'logical'
```
<!-- end_include -->

## Building a language

Cell provides more complex data structures using functions.  (More info
coming soon, but see Lisp's `cons` etc. for the general idea.)

## Details

mycode.cell --> [Lexing](lexing.md) --> [Parsing](parsing.md) --> [Evaluation](evaluation.md) --> [Library](library.md) -> Behaviour

