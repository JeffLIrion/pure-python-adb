"""Unit tests for `Connection` class.

"""


import asyncio
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, '..')

from ppadb.connection import Connection

from .async_wrapper import AsyncMock, awaiter
from .patchers import FakeStreamReader, FakeStreamWriter


class TestConnection(unittest.TestCase):
    @awaiter
    async def test_connect_close(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            conn = Connection()
            await conn.connect()
            self.assertIsNotNone(conn.reader)
            self.assertIsNotNone(conn.writer)

        await conn.close()
        self.assertIsNone(conn.reader)
        self.assertIsNone(conn.writer)

    @awaiter
    async def test_connect_close_catch_oserror(self):
        with patch('asyncio.open_connection', return_value=(FakeStreamReader(), FakeStreamWriter()), new_callable=AsyncMock):
            conn = Connection()
            await conn.connect()
            self.assertIsNotNone(conn.reader)
            self.assertIsNotNone(conn.writer)

        with patch('{}.FakeStreamWriter.close'.format(__name__), side_effect=OSError):
            await conn.close()
            self.assertIsNone(conn.reader)
            self.assertIsNone(conn.writer)

    @awaiter
    async def test_connect_with_timeout(self):
        with self.assertRaises(RuntimeError):
            with patch('asyncio.open_connection', side_effect=asyncio.TimeoutError, new_callable=AsyncMock):
                conn = Connection(timeout=1)
                await conn.connect()


if __name__ == '__main__':
    unittest.main()
