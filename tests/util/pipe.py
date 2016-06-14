
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

    def write(self, s):
        for ch in s:
            self.buffer.put(ch)

    def read(self, size=None):
        ret = ""
        while size is None or len(ret) < size:
            ret += self.buffer.get()
            if self.buffer.empty() and self.closed:
                break
        return ret

    def close(self):
        self.closed = True
