class Env:
    def __init__(self, parent=None, stdin=None, stdout=None, stderr=None):
        """
        Supply _either_ std{in,out,err} _or_ parent, not both.
        """
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.parent = parent
        if parent is not None:
            assert stdin is None
            assert stdout is None
            assert stderr is None
            self.stdin = parent.stdin
            self.stdout = parent.stdout
            self.stderr = parent.stderr
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

    def contains(self, name):
        return name in self.items

    def __str__(self):
        ret = ""
        for k, v in self.items.items():
            ret += "%s=%s\n" % (k, v)
        ret += ".\n" + str(self.parent)
        return ret
