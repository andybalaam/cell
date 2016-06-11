class Env:
    def __init__(self, parent=None):
        self.parent = parent
        self.items = {}

    def get(self, name):
        if name in self.items:
            return self.items[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None

    def set(self, name, value):
        self.items[name] = value

    def __str__(self):
        ret = ""
        for k, v in self.items.items():
            ret += "%s=%s\n" % (k, v)
        ret += ".\n" + str(self.parent)
        return ret
