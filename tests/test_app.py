import os
from unittest.mock import patch
from app.main import app
from app.models import Transaction
from sqlalchemy.orm import Session
from app.main import app
from app.models import Transaction
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from sqlalchemy.orm.exc import NoResultFound
from unittest.mock import patch

KAFKA_BROKER_HOST = os.getenv("KAFKA_BROKER_HOST")
KAFKA_BROKER_PORT = os.getenv("KAFKA_BROKER_PORT")

client = TestClient(app)

@patch('app.main.get_db', autospec=True)
def test_get_transaction_by_hash_not_found(mock_get_db):
    mock_db = mock_get_db.return_value
    mock_db.query.return_value.filter_by.return_value.one.side_effect = NoResultFound

    response = client.get("/transactions/non_existent_hash")

    expected_response = {"error": "Transaction not found"}
    assert response.json() == expected_response

def test_get_transaction_by_hash_found(db: Session):
    existing_hashes = db.query(Transaction.hash).filter(Transaction.hash.in_(["hash1", "hash2"])).all()
    existing_hashes = {hash for (hash,) in existing_hashes}

    mock_transactions = [
        Transaction(
            hash="hash1",
            fromAddress="from1",
            toAddress="to1",
            blockNumber=123,
            executionTimestamp="2023-08-01T07:05:23",
            gasUsed=678,
            gasCostInDollars=123456
        ),
        Transaction(
            hash="hash2",
            fromAddress="from2",
            toAddress="to2",
            blockNumber=124,
            executionTimestamp="2023-08-01T08:05:23",
            gasUsed=679,
            gasCostInDollars=123457
        )
    ]

    new_transactions = [tx for tx in mock_transactions if tx.hash not in existing_hashes]
    db.add_all(new_transactions)
    db.commit()

    response = client.get("/transactions/hash1")

    assert response.status_code == 200

    expected_response = {
        "id": 1,
        "hash": "hash1",
        "fromAddress": "from1",
        "toAddress": "to1",
        "blockNumber": 123,
        "executionTimestamp": "2023-08-01T07:05:23",
        "gasUsed": 678,
        "gasCostInDollars": 123456
    }
    assert response.json() == expected_response

def test_get_stats(db: Session):
    existing_hashes = db.query(Transaction.hash).filter(Transaction.hash.in_(["hash1", "hash2"])).all()
    existing_hashes = {hash for (hash,) in existing_hashes}

    mock_transactions = [
        Transaction(
            hash="hash1",
            fromAddress="from1",
            toAddress="to1",
            blockNumber=123,
            executionTimestamp="2023-08-01T07:05:23",
            gasUsed=678,
            gasCostInDollars=123456
        ),
        Transaction(
            hash="hash2",
            fromAddress="from2",
            toAddress="to2",
            blockNumber=124,
            executionTimestamp="2023-08-01T08:05:23",
            gasUsed=679,
            gasCostInDollars=123457
        )
    ]

    new_transactions = [tx for tx in mock_transactions if tx.hash not in existing_hashes]
    db.add_all(new_transactions)
    db.commit()

    response = client.get("/stats")
    assert response.status_code == 200
    assert response.json() == {
        "totalTransactionsInDB": 2,
        "totalGasUsed": 1357,
        "totalGasCostInDollars": 246913
    }

# def test_produce_to_kafka_endpoint():
#     response = client.get("/produce-to-kafka/")
#     assert response.status_code == 200
#     assert response.json() == {"status": "Data is being produced to Kafka in the background"}

# def test_consume_from_kafka_endpoint():
#     mock_messages = [
#         {"partition": 0, "offset": 0, "key": None, "value": "test_value_1"},
#         {"partition": 0, "offset": 1, "key": None, "value": "test_value_2"}
#     ]

#     mock_consume = MagicMock(return_value=mock_messages)
#     app.dependency_overrides[consume_from_kafka.__name__] = mock_consume

#     response = client.get("/consume-from-kafka/")
#     assert response.status_code == 200
#     assert response.json()

#     app.dependency_overrides.pop(consume_from_kafka.__name__)

