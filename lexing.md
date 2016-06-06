# Lexing in Cell

A lexer is a part of a programming language that turns characters in a text
file into "tokens" which are the basic building blocks of the language.  An
example of a token is the number `351`, which is made out of three characters:
"3", "5", and "1".

The lexer reads in characters one by one, and decides what type of token they
are, and then spits out tokens as it finds them.

You can find Cell's lexer at:
https://github.com/andybalaam/cell/blob/master/cell/lexer.py
and the tests for it at:
https://github.com/andybalaam/cell/blob/master/tests/lexer_tests.py .

## Cell's lexing rules

Cell programs only contain ASCII characters.

The types of tokens Cell recognises are:

* Numbers (containing `0`-`9` characters, and possibly one `.`).
* Strings (starting and ending with `"`, containing any other characters).
* Some special punctuation: `(),{};:=`.
* Arithmetic operations: `+-*/`.
* Symbols (starting with a letter, containing any letter, number or an
  underscore).
* Spaces and newlines, which are just used to separate tokens, and
  otherwise have no meaning (tabs are not allowed).

When Cell's lexer hits a character that is not allowed in the current token,
it ends this token, and starts another.  So, for example `print(` becomes two
tokens: the symbol `print` and the punctuation `(`.

