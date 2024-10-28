import unittest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from polkadot.polkadot import Polkadot
from polkadot.exceptions import PolkadotException

class TestPolkadot(unittest.TestCase):

    def setUp(self):
        self.polkadot = Polkadot(endpoint="wss://rpc.polkadot.io")

    @patch('polkadot.polkadot.SubstrateInterface')
    def test_connect_success(self, mock_substrate):
        self.polkadot.connect()
        mock_substrate.assert_called_once_with(
            url="wss://rpc.polkadot.io",
            ss58_format=0,
            type_registry_preset='polkadot'
        )

    @patch('polkadot.polkadot.SubstrateInterface')
    def test_connect_failure(self, mock_substrate):
        mock_substrate.side_effect = Exception("Connection failed")
        with self.assertRaises(PolkadotException):
            self.polkadot.connect()

    def test_ensure_connected(self):
        with patch.object(self.polkadot, 'connect') as mock_connect:
            self.polkadot.ensure_connected()
            mock_connect.assert_called_once()

    def test_close(self):
        mock_substrate = MagicMock()
        self.polkadot.substrate = mock_substrate

        # Call close
        self.polkadot.close()
        mock_substrate.close.assert_called_once()
        self.assertIsNone(self.polkadot.substrate)

    @patch('polkadot.polkadot.SubstrateInterface')
    def test_get_balance(self, mock_substrate):
        mock_query = MagicMock()
        mock_query.return_value = {
            'data': {
                'free': MagicMock(value=1000000000000)  # 100 DOT in planck
            }
        }
        mock_substrate.return_value.query = mock_query

        self.polkadot.connect()
        balance = self.polkadot.get_balance("test_address")
        
        self.assertEqual(balance, Decimal('100'))
        mock_query.assert_called_once_with('System', 'Account', ['test_address'])

    @patch('polkadot.polkadot.SubstrateInterface')
    def test_subscribe_events(self, mock_substrate):
        mock_events = [MagicMock(), MagicMock(), MagicMock()]
        mock_substrate.return_value.subscribe_events.return_value = mock_events

        self.polkadot.connect()
        events = list(self.polkadot.subscribe_events())
        
        self.assertEqual(events, mock_events)
        mock_substrate.return_value.subscribe_events.assert_called_once()

if __name__ == '__main__':
    unittest.main()