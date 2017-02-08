#!/usr/bin/env python
import asyncio
import unittest
from unittest import mock
from async_receive import receive


def _run(coro):
    """Run the given coroutine."""
    return asyncio.get_event_loop().run_until_complete(coro)

def AsyncMock(*args, **kwargs):
    """Create an async function mock."""
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


class TestReceive(unittest.TestCase):
    def test_invalid_packet(self):
        self.assertRaises(ValueError, _run, receive('FOO', 'data'))

    @mock.patch('async_receive.send_to_client', new=AsyncMock())
    def test_ping(self):
        _run(receive('PING', 'data'))
        from async_receive import send_to_client
        send_to_client.mock.assert_called_once_with('PONG', 'data')

    @mock.patch('async_receive.send_to_client', new=AsyncMock())
    @mock.patch('async_receive.trigger_event',
                new=AsyncMock(return_value='my response'))
    def test_message(self):
        _run(receive('MESSAGE', 'data'))
        from async_receive import send_to_client, trigger_event
        trigger_event.mock.assert_called_once_with('message', 'data')
        send_to_client.mock.assert_called_once_with('MESSAGE', 'my response')


if __name__ == '__main__':
    unittest.main()
