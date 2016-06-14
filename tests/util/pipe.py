
from queue import Queue


class Pipe:
    """
    In-memory file-like object that may be read and written by co-operating
    threads.
    Note: no readline() etc. is provided - only read and write.
    Note: read() will block waiting for more to be read, until close() is
    called.
    """
    def __init__(self):
        self.buffer = Queue()
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def write(self, s):
        for ch in s:
            self.buffer.put(ch)

    def read(self, size=None):
        ret = ""
        while size is None or len(ret) < size:
            if self.buffer.empty() and self.closed:
                break
            ret += self.buffer.get(timeout=0.1)
        return ret

    def readline(self):
        ret = ""
        c = "x"
        while c not in ("\n", ""):
            c = self.buffer.get(timeout=0.1)
            ret += c
            if self.buffer.empty() and self.closed:
                break
        return ret

    def flush(self):
        pass

    def close(self):
        self.closed = True
