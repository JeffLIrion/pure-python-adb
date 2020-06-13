"""Unit tests for `Client` class.

"""


import asyncio
import os
import sys
import unittest
from unittest.mock import mock_open, patch

sys.path.insert(0, '..')

from aio_ppadb.client import Client
from aio_ppadb.protocol import Protocol
from aio_ppadb.sync import Sync

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
    async def test_shell_error(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, return_value=b'FAIL'):
                with self.assertRaises(RuntimeError):
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
    async def test_push_file_not_found(self):
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(FileNotFoundError):
                await self.device.push('src', 'dest')

            with self.assertRaises(FileNotFoundError):
                sync = Sync('Unused')
                await sync.push('src', 'dest', 'mode')

    @awaiter
    async def test_push(self):
        def progress(*args, **kwargs):
            pass

        filedata = b'Ohayou sekai.\nGood morning world!'
        with patch('os.path.exists', return_value=True), patch('os.path.isfile', return_value=True), patch('aio_ppadb.device.open', mock_open(read_data=filedata)), patch('os.stat', return_value=os.stat_result((123,) * 10)), patch('aio_ppadb.sync.open', mock_open(read_data=filedata)):
            with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
                with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'OKAY', b'OKAY', PNG_IMAGE_NEEDS_REPLACING, b'', b'OKAY']):
                    await self.device.push('src', 'dest', progress=progress)

    @awaiter
    async def test_push_dir(self):
        with patch('os.path.exists', return_value=True), patch('os.path.isfile', return_value=False), patch('os.path.isdir', return_value=True), patch('os.walk', return_value=[('root1', 'dirs1', 'files1'), ('root2', 'dirs2', 'files2')]):
            with patch('aio_ppadb.device.Device.shell', new_callable=AsyncMock), patch('aio_ppadb.device.Device._push', new_callable=AsyncMock):
                await self.device.push('src', 'dest')

    @awaiter
    async def test_pull(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'OKAY', b'DATA', Sync._little_endian(4), b'TEST', b'DONE', b'OKAY']):
                with patch('aio_ppadb.sync.open', mock_open()):
                    #with self.assertRaises(RuntimeError):
                    await self.device.pull('src', 'dest')

    @awaiter
    async def test_pull_fail(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'OKAY', b'FAIL', Sync._little_endian(4), b'TEST', b'DONE', b'OKAY']):
                with patch('aio_ppadb.sync.open', mock_open()):
                    #with self.assertRaises(RuntimeError):
                    await self.device.pull('src', 'dest')


class TestProtocol(unittest.TestCase):
    def test_encode_decode_length(self):
        for i in range(16 ** 2):
            self.assertEqual(i, Protocol.decode_length(Protocol.encode_length(i)))


if __name__ == '__main__':
    unittest.main()
