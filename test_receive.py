#!/usr/bin/env python
import unittest
from unittest import mock
from receive import receive


class TestReceive(unittest.TestCase):
    def test_invalid_packet(self):
        self.assertRaises(ValueError, receive, 'FOO', 'data')

    @mock.patch('receive.send_to_client')
    def test_ping(self, send_to_client):
        receive('PING', 'data')
        send_to_client.assert_called_once_with('PONG', 'data')

    @mock.patch('receive.trigger_event', return_value='my response')
    @mock.patch('receive.send_to_client')
    def test_message(self, send_to_client, trigger_event):
        receive('MESSAGE', 'data')
        trigger_event.assert_called_once_with('message', 'data')
        send_to_client.assert_called_once_with('MESSAGE', 'my response')


if __name__ == '__main__':
    unittest.main()
