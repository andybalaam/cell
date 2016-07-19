
chars_in = """
chars_in =
    {:(s)
        impl =
            {:(s, i)
                if(equals(len(s), i),
                {
                    None;
                },
                {
                    {:( which )
                        if( equals( which, "f" ),
                        {
                            char_at(i, s);
                        },
                        {
                            impl(s, i + 1);
                        });
                    };
                });
            };
        impl(s, 0);
    };
"""
