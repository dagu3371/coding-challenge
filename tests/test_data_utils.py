from app.utils import calculate_execution_timestamp
from app.models import Transaction
from app.data_utils import process_csv_row

def test_process_csv_row_valid():
    row = {
        "hash": "test_hash",
        "from_address": "test_from",
        "to_address": "test_to",
        "block_number": "test_block",
        "transaction_index": 2,
        "block_timestamp": "2023-08-01 07:04:59.000000 UTC"
    }

    expected_transaction = Transaction(
        hash="test_hash",
        fromAddress="test_from",
        toAddress="test_to",
        blockNumber="test_block",
        executionTimestamp=calculate_execution_timestamp(row["block_timestamp"], row["transaction_index"]).isoformat()  # Format timestamp to match the model
    )

    result = process_csv_row(row)
    assert result == expected_transaction.dict()
