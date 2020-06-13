"""Patches for async socket functionality."""

from contextlib import contextmanager


class FakeStreamWriter:
    def close(self):
        pass

    async def wait_closed(self):
        pass

    def write(self, data):
        pass

    async def drain(self):
        pass


class FakeStreamReader:
    async def read(self, numbytes):
        return b'TEST'


class FileReadWrite(object):
    """Mock an opened file that can be read and written to."""
    def __init__(self):
        self._content = b''
        self._mode = 'r'

    def read(self):
        if self._mode == 'r':
            if not isinstance(self._content, str):
                return self._content.decode()
            return self._content

        if isinstance(self._content, str):
            return self._content.encode('utf-8')
        return self._content
        

    def write(self, content):
        self._content = content


PRIVATE_KEY = FileReadWrite()
PUBLIC_KEY = FileReadWrite()


@contextmanager
def open_priv_pub(infile, mode='r'):
    try:
        if infile.endswith('.pub'):
            PUBLIC_KEY._mode = mode
            yield PUBLIC_KEY
        else:
            PRIVATE_KEY._mode = mode
            yield PRIVATE_KEY
    finally:
        pass
