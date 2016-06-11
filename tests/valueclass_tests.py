
from tests.util.asserts import assert_that, equals, is_not, fail
from tests.util.test import test

from pycell.valueclass import valueclass


@test
def Can_construct_an_empty_value_class():
    @valueclass()
    class MyClass:
        pass

    MyClass()


@test
def Empty_value_classes_compare_equal_if_same_class():
    @valueclass()
    class MyClass:
        pass

    assert_that(MyClass(), equals(MyClass()))


@test
def Empty_value_classes_compare_not_equal_if_different_class():
    @valueclass()
    class MyClass1:
        pass

    @valueclass()
    class MyClass2:
        pass

    assert_that(MyClass1(), is_not(MyClass2()))


@test
def Can_construct_a_nonempty_value_class_using_positional_args():
    @valueclass("mem1", "mem2")
    class MyClass:
        pass

    b = MyClass(3, 4)
    assert_that(b.mem1, equals(3))
    assert_that(b.mem2, equals(4))


@test
def Can_construct_a_nonempty_value_class_using_keyword_args():
    @valueclass("mem1", "mem2")
    class MyClass:
        pass

    b = MyClass(mem1=3, mem2=4)
    assert_that(b.mem1, equals(3))
    assert_that(b.mem2, equals(4))


@test
def Constructing_an_empty_value_class_with_some_args_is_an_error():
    @valueclass()
    class MyClass:
        pass

    class BareClass:
        pass

    try:
        MyClass(3, 4)
        fail("Should have thrown")
    except TypeError as e1:
        try:
            BareClass(3, 4)
            fail("Should have thrown")
        except TypeError as e2:
            assert_that(str(e1), equals(str(e2)))


@test
def Constructing_with_too_few_args_is_an_error():
    @valueclass("foo", "bar")
    class MyClass:
        pass

    class BareClass:

        def __init__(self, foo, bar):
            pass

    try:
        MyClass(3)
        fail("Should have thrown")
    except TypeError as e1:
        try:
            BareClass(3)
            fail("Should have thrown")
        except TypeError as e2:
            assert_that(str(e1), equals(str(e2)))


@test
def Constructing_with_too_many_args_is_an_error():
    @valueclass("foo", "bar")
    class MyClass:
        pass

    class BareClass:

        def __init__(self, foo, bar):
            pass

    try:
        MyClass(3, 4, 5)
        fail("Should have thrown")
    except TypeError as e1:
        try:
            BareClass(3, 4, 5)
            fail("Should have thrown")
        except TypeError as e2:
            assert_that(str(e1), equals(str(e2)))


@test
def Constructing_with_unknown_keyword_arg_is_an_error():
    @valueclass("foo", "bar")
    class MyClass:
        pass

    class BareClass:

        def __init__(self, foo, bar):
            pass

    try:
        MyClass(foo=3, bar=4, baz=5)
        fail("Should have thrown")
    except TypeError as e1:
        try:
            BareClass(foo=3, bar=4, baz=5)
            fail("Should have thrown")
        except TypeError as e2:
            assert_that(str(e1), equals(str(e2)))


@test
def Constructing_with_repeat_of_positional_arg_as_keyword_is_an_error():
    @valueclass("foo", "bar")
    class MyClass:
        pass

    class BareClass:

        def __init__(self, foo, bar):
            pass

    try:
        MyClass(3, 4, bar=5)
        fail("Should have thrown")
    except TypeError as e1:
        try:
            BareClass(3, 4, bar=5)
            fail("Should have thrown")
        except TypeError as e2:
            assert_that(str(e1), equals(str(e2)))


@test
def Values_of_the_same_type_with_the_same_members_are_equal():
    @valueclass("m1", "m2", "m3")
    class MyClass:
        pass

    assert_that(MyClass("a", 3, None), equals(MyClass(m1="a", m2=3, m3=None)))


@test
def Values_of_the_same_type_with_different_members_are_not_equal():
    @valueclass("m1", "m2", "m3")
    class MyClass:
        pass

    assert_that(MyClass("a", 3, None), is_not(MyClass("a", 4, None)))


@test
def Values_of_different_types_with_the_same_members_are_not_equal():
    @valueclass("m1", "m2", "m3")
    class MyClass1:
        pass

    @valueclass("m1", "m2", "m3")
    class MyClass2:
        pass

    assert_that(MyClass1("a", 3, None), is_not(MyClass2("a", 3, None)))


@test
def The_repr_of_an_empty_value_can_be_used_to_make_an_equal_one():
    @valueclass()
    class MyClass:
        pass

    x = MyClass()
    x_repr = repr(x)
    y = eval(x_repr)
    assert_that(x, equals(y))


@test
def The_repr_of_a_nonempty_value_can_be_used_to_make_an_equal_one():
    @valueclass("m1", "m2", "m3")
    class MyClass:
        pass

    x = MyClass(3, '4', 5)
    x_repr = repr(x)
    y = eval(x_repr)
    assert_that(x, equals(y))


@test
def The_str_of_a_value_is_its_repr():
    @valueclass("m1", "m2", "m3")
    class MyClass:
        pass

    x = MyClass(3, '4', 5)
    assert_that(str(x), equals(repr(x)))
