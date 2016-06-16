# Objects in Cell

It is possible to use the fact that functions carry their own values
around with them (in so-called "closures") to construct trees of functions
that return functions that work quite like objects from languages like C++
or Java.

For example, we can write a function `open_account` that we can use
like this:

```
acc1 = open_account();
acc2 = open_account();

acc1("deposit")(10.25);
acc1("withdraw")(0.75);

acc2("deposit")(5.42);

print("acc1 balance=");
print(acc1("balance"));
print("");

print("acc2 balance=");
print(acc2("balance"));
```

and it will store the value of the account balance inside the acc1 and acc2
functions, so the output looks like this:

<!-- include "examples/bank_account.output.txt" -->
```
acc1 balance=
9.5

acc2 balance=
5.42
```
<!-- end_include -->

The magic to do this looks quite complicated, but once you understand
the syntax, and the fact that we can pass functions around as values
and call them later, it is reasonably simple:

```
open_account = {
    {
        bal = 0.0;
        {:(method_name)
            if(equals("deposit", method_name),
            {{:(amount)
                set("bal", bal + amount);
            }},
            {
                if(equals("withdraw", method_name),
                {{:(amount)
                    set("bal", bal - amount);
                }},
                {
                    if(equals("balance", method_name),
                        {bal;},
                        {print("Unknown method!");}
                    );
                });
            })
        };
    }();
};
```

`bank_account` is a function that creates a function containing a value
called `bal`.  It immediately calls that function and returns the answer.

The answer is itself a function (that takes an argument `method_name`).
This function has a reference to the `bal` value, and can modify it, which
is what happens when we call the functions returned when we supply a method
name like "deposit".

If you can get your head around this, you understand closures, and, for
good measure, you can understand that "objects" and "closures" are in some
sense equivalent.
