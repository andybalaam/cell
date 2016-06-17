
pairs = """
pair =
    {:( f, s )
        {:( which )
            if( equals( which, "f" ),
                {f;},
                {s;}
            );
        };
    };

first = {:(p) p("f");};

second = {:(p) p("s");};
"""
