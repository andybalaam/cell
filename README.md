# This page has moved

*This repo has been moved to https://gitlab.com/cell_lang/cell (because GitLab is at least partially Free Software)*

*This file is at https://gitlab.com/cell_lang/cell/blob/master/README.md*

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

## Install

```
sudo apt-get install python3
git clone git@github.com:andybalaam/cell.git
cd cell
./cell                  # - to run the interactive environment
./cell filename.cell    # - to run a program
make                    # - to run all the tests
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
* A special "None" value

That's about it.

## Interacting with Cell

Cell has an interactive environment ("REPL") which can be launched by running
the Cell program with no arguments:

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

## How to write Cell programs

See the explanation of [Cell Syntax](syntax.md), and [The if function](if.md).

## Building a language

Cell does not provide special syntax for things like lists, maps and
objects, but they can be built up using the features of Cell functions.

The Cell library contains functions like `pair` that makes a simple data
structure from two values (more explanation at
[Data Structures](data_structures.md) ).

You can also build things that behave like objects in languages like Java and
C++ out of functions.  There is more explanation at: [Objects](objects.md).

## Explanations

Cell is designed to be useful to teach people how to write programming
languages, so the source code is intentionally short and hopefully reasonably
easy to read.  To get started, follow the links below for explanations of the
main parts.

In an interpreter, the program flows through several layers, starting off as
textual source code, and being transformed by each layer.

The first layer is the [Lexer](lexing.md), which reads in text characters, and
spits out "tokens" like `print`, or `{`.

The second layer is the [Parser](parsing.md), which reads in tokens, and spits
out tree-structures which it does not understand.

The third layer is the [Evaluator](evaluation.md), which reads in the tree
structures, understands them and "runs" them - turns them into concrete values
by looking up symbols, calling functions, and obeying rules (e.g. the rules of
arithmetic).

While the Evaluator is running, it has access to the [Library](library.md),
which is a set of standard values and functions that all programs can use.

## See also

* [Video series about how to write a programming language](https://www.youtube.com/watch?v=TG0qRDrUPpA&list=PLgyU3jNA6VjT3FW83eHqryNcqd6fsvdrv)
* [Articles on how to write a programming language](https://github.com/andybalaam/articles-how-to-write-a-programming-language/) (now published in the [Overload](https://accu.org/index.php/journals/c78/) journal issues 145, 146 and 147).
* [My ACCU Conference talk about Cell](https://www.youtube.com/watch?v=82-XjMzKaC8)
* [Slides for the videos](https://github.com/andybalaam/videos-writing-cell)
* [datecalc](https://github.com/andybalaam/datecalc) - an even smaller language
