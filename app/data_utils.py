import csv
import os
import logging
import json
import time
from .models import Transaction
from .kafka_utils import produce_to_kafka
from .utils import calculate_execution_timestamp, get_eth_price_at_timestamp, compute_dollar_cost

logging.basicConfig(level=logging.INFO)
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, '..', 'data', 'ethereum_txs.csv')

def process_csv_row(row):
    execution_timestamp = calculate_execution_timestamp(
        row.get('block_timestamp', ''),
        int(row.get('transaction_index', 0)),
    ).isoformat()
    eth_price = get_eth_price_at_timestamp(execution_timestamp)
    gas_used = int(row.get('receipts_gas_used', ''))
    gas_price = int(row.get('gas_price', ''))
    gas_cost_dollars = compute_dollar_cost(gas_used, gas_price, eth_price)
    filtered_data = {
        'hash': row.get('hash', ''),
        'fromAddress': row.get('from_address', ''),
        'toAddress': row.get('to_address', ''),
        'blockNumber': row.get('block_number', ''),
        'executionTimestamp': execution_timestamp,
        'gasUsed': gas_used,
        'gasCostInDollars': gas_cost_dollars,
    }
    try:
        transaction_data = serialize_transaction(filtered_data)
        return transaction_data
    except Exception as e:
        exception_type = type(e).__name__
        raise ValueError(f"Failed to process a row {filtered_data} due to {exception_type}: {e}")

def serialize_transaction(transaction: Transaction):
    return json.dumps(transaction, default=str)

def produce_data_to_kafka(producer):
    with open(csv_path, 'r') as f:
        csv_reader = csv.DictReader(f)
        next(csv_reader)
        transactions_produced = 0
        for row in csv_reader:
            transaction_data = process_csv_row(row)
            if transaction_data:
                produce_to_kafka(producer, 'ethereum_transactions', transaction_data)
                transactions_produced += 1

                if transactions_produced >= 20:
                    transactions_produced = 0
                    time.sleep(60)  # Sleep for 1 minute to bypass Coingecko rate limit