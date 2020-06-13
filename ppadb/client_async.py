from .command.host import Host
from .connection import Connection


class ClientAsync(Host):
    def __init__(self, host='127.0.0.1', port=5037):
        self.host = host
        self.port = port

    async def create_connection(self, timeout=None):
        conn = Connection(self.host, self.port, timeout)
        return await conn.connect()

    async def device(self, serial):
        devices = await self.devices()

        for device in devices:
            if device.serial == serial:
                return device

        return None
