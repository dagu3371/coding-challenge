import csv
import os
from .models import Transaction
from .kafka_utils import produce_to_kafka

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, '..', 'data', 'ethereum_txs.csv')

def process_csv_row(row):
    filtered_data = {
        'hash': row.get('hash', ''),
        'fromAddress': row.get('from_address', ''),
        'toAddress': row.get('to_address', ''),
        'blockNumber': row.get('block_number', '')
    }
    try:
        transaction = Transaction(**filtered_data)
        return transaction.dict()
    except Exception as e:
        exception_type = type(e).__name__
        raise ValueError(f"Failed to process a row {filtered_data} due to {exception_type}: {e}")

def produce_data_to_kafka(producer):
    with open(csv_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        next(csv_reader)
        for row in csv_reader:
            transaction_data = process_csv_row(row)
            if transaction_data:
                produce_to_kafka(producer, 'ethereum_transactions', transaction_data)
