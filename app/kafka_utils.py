from kafka import KafkaConsumer
import json

def produce_to_kafka(producer, topic, data):
    transaction_bytes = json.dumps(data).encode('utf-8')
    producer.send(topic, value=transaction_bytes)

def consume_from_kafka(topic, num_messages=10):
    messages = []

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='kafka:9092',
        group_id='my-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )

    for _ in range(num_messages):
        message = next(consumer)
        messages.append({"partition": message.partition,
                         "offset": message.offset,
                         "key": message.key,
                         "value": message.value})

    consumer.close()
    return messages
