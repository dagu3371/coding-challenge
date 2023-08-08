from app.utils import calculate_execution_timestamp
from app.models import Transaction
from app.data_utils import process_csv_row
import unittest.mock as mock

@mock.patch('app.utils.compute_dollar_cost')
def test_process_csv_row_valid(mock_compute_dollar_cost):
    mock_compute_dollar_cost.return_value = 42
    row = {
        "hash": "test_hash",
        "from_address": "test_from",
        "to_address": "test_to",
        "block_number": "test_block",
        "transaction_index": 2,
        "block_timestamp": "2023-08-01 07:04:59.000000 UTC",
        "receipts_gas_used": 2,
        "gas_price": 2,
    }

    expected_transaction = Transaction(
        hash="test_hash",
        fromAddress="test_from",
        toAddress="test_to",
        blockNumber="test_block",
        executionTimestamp=calculate_execution_timestamp(row["block_timestamp"], row["transaction_index"]).isoformat(),
        gasUsed=2,
        gasCostInDollars=7
    )

    result = process_csv_row(row)
    assert result == expected_transaction.dict()
