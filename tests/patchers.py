"""Patches for async socket functionality."""


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
