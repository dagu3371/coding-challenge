import os
from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.kafka_utils import consume_from_kafka

KAFKA_BROKER_HOST = os.getenv("KAFKA_BROKER_HOST")
KAFKA_BROKER_PORT = os.getenv("KAFKA_BROKER_PORT")

client = TestClient(app)

def test_produce_to_kafka_endpoint():
    response = client.get("/produce-to-kafka/")
    assert response.status_code == 200
    assert response.json() == {"status": "Data is being produced to Kafka in the background"}

def test_consume_from_kafka_endpoint():
    mock_messages = [
        {"partition": 0, "offset": 0, "key": None, "value": "test_value_1"},
        {"partition": 0, "offset": 1, "key": None, "value": "test_value_2"}
    ]

    mock_consume = MagicMock(return_value=mock_messages)
    app.dependency_overrides[consume_from_kafka.__name__] = mock_consume

    response = client.get("/consume-from-kafka/")
    assert response.status_code == 200
    assert response.json()

    app.dependency_overrides.pop(consume_from_kafka.__name__)

