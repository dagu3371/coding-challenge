from app.data_utils import process_csv_row

def test_process_csv_row_valid():
    row = {
        'hash': 'test_hash',
        'from_address': 'test_from',
        'to_address': 'test_to',
        'block_number': '12345'
    }
    result = process_csv_row(row)
    assert result is not None
    assert isinstance(result, dict)
    assert result['hash'] == 'test_hash'
    assert result['fromAddress'] == 'test_from'
    assert result['toAddress'] == 'test_to'
    assert result['blockNumber'] == '12345'
