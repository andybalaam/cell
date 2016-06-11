
class Iterator:

    @staticmethod
    def implements(obj):
        try:
            iter(obj)
            return True
        except:
            return False
