
chars_in = """
chars_in =
    {:(s)
        impl =
            {:(s, i)
                {:( which )
                    if( equals( which, "f" ),
                    {
                        ch = char_at(i, s);
                        ch;
                    },
                    {
                        if( equals( len(s), i + 1 ),
                            {},
                            {impl(s, i + 1);}
                        );
                    }
                    );
                };
            };
        impl(s, 0);
    };
"""
