from app.kafka_utils import produce_to_kafka, deserialize_transaction
from app.models import Transaction
import json

def test_produce_to_kafka():
    class MockProducer:
        def send(self, topic, value):
            self.topic = topic
            self.value = value
    mock_producer = MockProducer()

    data = {"hash": "test_hash", "fromAddress": "test_from", "toAddress": "test_to", "blockNumber": "123"}
    produce_to_kafka(mock_producer, 'test_topic', data)

    assert mock_producer.topic == 'test_topic'
    assert mock_producer.value == b'{"hash": "test_hash", "fromAddress": "test_from", "toAddress": "test_to", "blockNumber": "123"}'


def test_deserialize_transaction():
    data = "{\"hash\": \"0x6f218a5e009c56f8db17e933af7cc98360b699ae88cb85ef31c3eb351ecdee24\", \"fromAddress\": \"0x62caee1f532bea1135733a909f1cbe4e0abf282b\", \"toAddress\": \"0x3999d2c5207c06bbc5cf8a6bea52966cabb76d41\", \"blockNumber\": \"17818542\", \"executionTimestamp\": \"2023-08-01T07:05:11\", \"gasUsed\": 164465, \"gasCostInDollars\": 7614632759412343}"
    data_dict = json.loads(data)
    expected_transaction = Transaction(**data_dict)
    assert deserialize_transaction(data) == expected_transaction