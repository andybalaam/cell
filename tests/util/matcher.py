
class Matcher:

    @staticmethod
    def implements(obj):
        dt = obj.__class__.__dict__
        return (
                "matches" in dt
            and "description" in dt
        )
