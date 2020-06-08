"""Unit tests for `Client` class.

"""


import asyncio
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, '..')

from aio_ppadb.client import Client

from .async_wrapper import AsyncMock, awaiter
from .patchers import FakeStreamReader, FakeStreamWriter


PNG_IMAGE = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\n\x00\x00\x00\n\x08\x06\x00\x00\x00\x8d2\xcf\xbd\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\tpHYs\x00\x00\x0fa\x00\x00\x0fa\x01\xa8?\xa7i\x00\x00\x00\x0eIDAT\x18\x95c`\x18\x05\x83\x13\x00\x00\x01\x9a\x00\x01\x16\xca\xd3i\x00\x00\x00\x00IEND\xaeB`\x82'

PNG_IMAGE_NEEDS_REPLACING = PNG_IMAGE[:5] + b'\r' + PNG_IMAGE[5:]


class TestDevice(unittest.TestCase):
    @awaiter
    async def setUp(self):
        self.client = Client()

        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'000b', b'serial test']):
                self.device = await self.client.device('serial')

    @awaiter
    async def test_shell(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'OKAY', b'test', b'', b'OKAY']):
                self.assertEqual(await self.device.shell('TEST'), 'test')

    @awaiter
    async def test_screencap(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'OKAY', PNG_IMAGE, b'', b'OKAY']):
                self.assertEqual(await self.device.screencap(), PNG_IMAGE)

        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'OKAY', PNG_IMAGE_NEEDS_REPLACING, b'', b'OKAY']):
                self.assertEqual(await self.device.screencap(), PNG_IMAGE)

    @awaiter
    async def test_pull(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'OKAY', b'test', b'', b'OKAY']):
                self.assertEqual(await self.device.shell('TEST'), 'test')

'''async def shell(self, cmd, handler=None, timeout=None):
        conn = await self.create_connection(timeout=timeout)

        cmd = "shell:{}".format(cmd)
        await conn.send(cmd)

        if handler:
            handler(conn)
        else:
            result = await conn.read_all()
            await conn.close()
            return result.decode('utf-8')'''


if __name__ == '__main__':
    unittest.main()
