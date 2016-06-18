# Cell Syntax

## Semi-colons

Every statement you type in Cell must end with a semi-colon (`;`).  Combined
with the fact that Cell encourages you to write lots of short statements,
this means you may see a lot more semi-colons than you are used to!

The basic idea is that you must type a semi-colon whenever you've finished
writing a value that you want to be returned or referred to by a symbol.
A good rule of thumb is that whenever you are going to write a `}` you
probably want a `;` first, and whenever you've finished a command, it should
end with a `;`.

## Simple types

Numbers and strings in Cell work as in many other languages:

<!-- include "examples/numbers_and_strings.cellsession" -->
```
>>> 3;
3
>>> 20.5 + 12;
32.5
>>> "foo";
'foo'
>>> 'bar';
'bar'
```
<!-- end_include -->

## Calling functions

To call a function, we just write its name, then the arguments we want to pass,
separated by commas.  This is similar to many other languages like Python, C,
C++, Java and JavaScript:

<!-- include "examples/calling_functions.cell" -->
```
print("Hello!");
```
<!-- end_include -->

Running the above program produces:

<!-- include "examples/calling_functions.output.txt" -->
```
Hello!
```
<!-- end_include -->

as you might expect.

## Creating functions

A function is defined by enclosing some code in curly braces `{}`.  So, a
simple function that prints a message looks like this:

<!-- include "examples/function_message.cell" -->
```
{
    print("Welcome to the world of...");
    print("Cell Adventures!");
    print("");
    print("Press any key to continue.");
};
```
<!-- end_include -->

### Naming functions

The code above defines a function, but doesn't give it a name, so we can't
call it!  To name it, we use `=`, like when we are naming any other value:

<!-- include "examples/function_naming.cell" -->
```
welcome_message = {
    print("Welcome, adventurer.");
    print("The system awaits your command...");
};
```
<!-- end_include -->

### Returning answers

Sometimes you need to return an answer from a function.  Cell functions
don't need a `return` keyword or similar - they just return the last line
of the function, so this function:

<!-- include "examples/function_return.cell" -->
```
square_half = {
    x = 1 / 2;
    x * x;
};
```
<!-- end_include -->

Will return `0.25` because the last line is `x * x`.

So to call this function and store the return value in another variable,
we do:

```
the_answer = square_half();
```

### Passing in arguments

Of course, you often want to pass information in to functions using arguments.
to do that, we add a `:` at the beginning, and then a list of arguments
inside some brackets:

<!-- include "examples/function_with_args.cell" -->
```
sum_of_squares = {:(x, y)
    sqx = x * x;
    sqy = y * y;
    sqx + sqy;
};
```
<!-- end_include -->

## Passing functions around

You can call a function immediately, instead of giving it a name, by putting
`()` straight after it:

<!-- include "examples/function_immediate.cell" -->
```
{
    print("Camera 1");
    print("Camera 2");
}();
```
<!-- end_include -->

This program runs the function straight away, so it prints the message:

<!-- include "examples/function_immediate.output.txt" -->
```
Camera 1
Camera 2
```
<!-- end_include -->

This gives you a clue that functions are just values like numbers and strings,
so you can treat them the same way as any other value.  One useful thing
you can do is pass them in to functions, and return them from functions.
Let's start by passing some in:

<!-- include "examples/function_passed_as_argument.cell" -->
```
f1 = {
    print( "I am f1." );
};

f2 = {
    print( "And I am f2." );
};

do_both = {:(x, y)
    x();
    y();
};

do_both(f1, f2);
```
<!-- end_include -->

In the code above, we create two functions `f1` and `f2`, and then another
function `do_both`.  `do_both` takes two arguments, and uses `()` to call
them.  So when we run this program, even though we did not explicitly call
`f1` and `f2`, they do run because they were passed in to `do_both` (on the
last line) and `do_both` calls them:

<!-- include "examples/function_passed_as_argument.output.txt" -->
```
I am f1.
And I am f2.
```
<!-- end_include -->

By passing functions as arguments to other functions, and returning functions
from other functions we can do clever things like
[Data Structures](data_structures.md) and [Objects](objects.md).


