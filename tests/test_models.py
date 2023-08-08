from app.models import Transaction
import pytest

def test_transaction_model():
    data = {
        "hash": "test_hash",
        "fromAddress": "test_from",
        "toAddress": "test_to",
        "blockNumber": "test_block",
        "executionTimestamp": "test_timestamp"
    }
    transaction = Transaction(**data)
    assert transaction.hash == "test_hash"
    assert transaction.fromAddress == "test_from"
    assert transaction.toAddress == "test_to"
    assert transaction.blockNumber == "test_block"
    assert transaction.executionTimestamp == "test_timestamp"
