import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
BLOCK_LENGTH = 12
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range"

def calculate_execution_timestamp(block_timestamp, transaction_index):
    block_timestamp = datetime.strptime(block_timestamp, "%Y-%m-%d %H:%M:%S.%f %Z")
    transaction_timestamp = block_timestamp + timedelta(seconds=transaction_index * BLOCK_LENGTH)
    return transaction_timestamp

def get_eth_price_at_timestamp(timestamp):
    timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    unix_timestamp = int(timestamp.timestamp())
    url = COINGECKO_URL

    params = {
        "vs_currency": "usd",
        "from": unix_timestamp,
        "to": unix_timestamp + 3600
    }
    logging.info(params)
    response = requests.get(url, params=params)
    data = response.json()
    logging.info(data)
    if data and "prices" in data:
        eth_price = data["prices"][0][1]
        return eth_price

    return None

def compute_dollar_cost(gas_used, gas_price, eth_price):
    gas_cost_wei = gas_used * gas_price
    gas_cost_eth = gas_cost_wei / 1e18
    gas_cost_dollars = gas_cost_eth * eth_price
    return gas_cost_dollars