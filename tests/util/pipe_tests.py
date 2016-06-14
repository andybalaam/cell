
from threading import Thread

from tests.util.asserts import assert_that, equals
from tests.util.test import test
from tests.util.pipe import Pipe

@test
def What_you_write_in_you_can_read_out():
    pipe = Pipe()
    pipe.write("foo")
    pipe.close()
    assert_that(pipe.read(), equals("foo"))

@test
def Multiple_writes_can_be_read_together():
    pipe = Pipe()
    pipe.write("foo\n")
    pipe.write("bar\n")
    pipe.close()
    assert_that(pipe.read(), equals("foo\nbar\n"))

@test
def Read_can_ask_for_only_some_chars():
    pipe = Pipe()
    pipe.write("abcdef")
    pipe.close()
    assert_that(pipe.read(3), equals("abc"))
    assert_that(pipe.read(2), equals("de"))

@test
def Can_read_in_one_thread_and_write_in_another():
    pipe = Pipe()
    def writer(p):
        for i in range(1):
            p.write(str(i))
            p.write("\n")
        p.close()
    thread1 = Thread(target=writer, args=(pipe,))
    thread1.start()
    for i in range(1):
        x = pipe.read(len(str(i))+1)
        assert_that(x, equals(str(i)+"\n"))
    thread1.join()
