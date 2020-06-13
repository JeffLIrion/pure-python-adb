import asyncio

try:
    from unittest.mock import AsyncMock
except ImportError:
    from unittest.mock import MagicMock

    class AsyncMock(MagicMock):
        async def __call__(self, *args, **kwargs):
            return super(AsyncMock, self).__call__(*args, **kwargs)


def _await(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def awaiter(func):
    def sync_func(*args, **kwargs):
        return _await(func(*args, **kwargs))

    return sync_func
