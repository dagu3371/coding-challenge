from datetime import datetime, timedelta

BLOCK_LENGTH = 12

def calculate_execution_timestamp(block_timestamp, transaction_index):
    block_timestamp = datetime.strptime(block_timestamp, "%Y-%m-%d %H:%M:%S.%f %Z")
    transaction_timestamp = block_timestamp + timedelta(seconds=transaction_index * BLOCK_LENGTH)
    return transaction_timestamp