
def assert_implements(obj, interface):
    if interface == object:
        return
    elif not interface.implements(obj):
        raise AssertionError(
            "Object "
            + str(obj)
            + " does not implement interface "
            + interface.__name__
        )
