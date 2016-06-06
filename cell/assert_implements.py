
def assert_implements(obj, interface):
    if interface == object:
        return
    elif hasattr(interface, "implements"):
        if not interface.implements(obj):
            raise AssertionError(
                "Object "
                + str(obj)
                + " does not implement interface "
                + interface.__name__
                + "."
            )
    else:
        required = set(interface.required_members())
        existing = set(obj.__class__.__dict__.keys())
        missing = required - existing
        if len(missing) > 0:
            raise AssertionError(
                "Object "
                + str(obj)
                + " does not implement interface "
                + interface.__name__
                + ".  Missing members: "
                + str(missing)
            )
