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


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    @awaiter
    async def test_create_connection_fail(self):
        with self.assertRaises(RuntimeError):
            await self.client.create_connection()

    @awaiter
    async def test_device_returns_none(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'0000', b'']):
                self.assertIsNone(await self.client.device('serial'))

    @awaiter
    async def test_device(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            with patch('{}.FakeStreamReader.read'.format(__name__), new_callable=AsyncMock, side_effect=[b'OKAY', b'000b', b'serial test']):
                self.assertIsNotNone(await self.client.device('serial'))


if __name__ == '__main__':
    unittest.main()
