from cell.assert_implements import assert_implements
from cell.readable import Readable


def chars_in_file(f):
    """
    Provides an iterator through all the characters in a file, individually.
    """
    assert_implements(f, Readable)
    ch = f.read(1)
    while ch != "":
        yield ch
        ch = f.read(1)
