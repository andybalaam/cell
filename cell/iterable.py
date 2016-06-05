
class Iterable:

    @staticmethod
    def implements(obj):
        dt = obj.__class__.__dict__
        return (
            "__iter__" in dt
        )
