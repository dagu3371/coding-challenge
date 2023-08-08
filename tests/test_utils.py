from app.models import Transaction
from app.utils import calculate_execution_timestamp
from datetime import datetime, timedelta

BLOCK_LENGTH = 12

def test_calculate_execution_timestamp():
    block_timestamp = "2023-08-01 07:04:59.000000 UTC"
    transaction_index = 1
    expected_timestamp = datetime.strptime(block_timestamp, "%Y-%m-%d %H:%M:%S.%f %Z") + timedelta(seconds=transaction_index * BLOCK_LENGTH)
    calculated_timestamp = calculate_execution_timestamp(block_timestamp, transaction_index)
    assert calculated_timestamp == expected_timestamp

    block_timestamp = "2023-08-02 10:00:00.000000 UTC"
    transaction_index = 3
    expected_timestamp = datetime.strptime(block_timestamp, "%Y-%m-%d %H:%M:%S.%f %Z") + timedelta(seconds=transaction_index * BLOCK_LENGTH)
    calculated_timestamp = calculate_execution_timestamp(block_timestamp, transaction_index)
    assert calculated_timestamp == expected_timestamp
