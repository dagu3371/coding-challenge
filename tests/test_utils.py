from app.utils import get_eth_price_at_timestamp, calculate_execution_timestamp, compute_dollar_cost
from datetime import datetime, timedelta
import unittest.mock as mock

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

@mock.patch('app.utils.requests.get')
def test_get_eth_price_at_timestamp(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"prices": [[1677782400000, 3000]]}

    mock_get.return_value = mock_response

    timestamp = "2023-08-01T07:05:23"
    eth_price = get_eth_price_at_timestamp(timestamp)

    assert eth_price == 3000

def test_compute_dollar_cost():
    eth_price = 3000
    gas_used = 12345678
    gas_price = 23759
    gas_cost_wei = gas_used * gas_price
    gas_cost_eth = gas_cost_wei / 1e18
    expected_cost = gas_cost_eth * eth_price
    assert compute_dollar_cost(gas_used, gas_price, eth_price) == expected_cost