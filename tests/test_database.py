import unittest
from unittest.mock import patch, Mock
from sqlalchemy.orm import Session
from app.database import create_transaction_db

class TestDatabaseFunctions(unittest.TestCase):

    @patch('app.database.SessionLocal', autospec=True)
    def test_create_transaction_db(self, mock_session_local):
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session

        mock_transaction = Mock()
        mock_transaction_dict = {
            'hash': 'test_hash',
            'from_address': 'test_from',
            'to_address': 'test_to',
            'block_number': 'test_block',
            'execution_timestamp': '2023-08-01T07:05:23',
            'gas_used': 12345,
            'gas_cost_in_dollars': 6789
        }
        mock_transaction.dict.return_value = mock_transaction_dict

        result = create_transaction_db(mock_transaction)

        created_transaction = mock_session.add.call_args[0][0]
        self.assertEqual(created_transaction.hash, 'test_hash')
        self.assertEqual(created_transaction.from_address, 'test_from')
        self.assertEqual(created_transaction.to_address, 'test_to')

        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(created_transaction)
        mock_session.close.assert_called_once()

        self.assertEqual(result, created_transaction)
