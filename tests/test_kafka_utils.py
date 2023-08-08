from app.kafka_utils import produce_to_kafka

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