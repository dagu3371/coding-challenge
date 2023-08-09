from kafka import KafkaConsumer
from app.database import create_transaction_db
from app.models import Transaction
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def produce_to_kafka(producer, topic, data):
    transaction_bytes = json.dumps(data).encode('utf-8')
    producer.send(topic, value=transaction_bytes)

def deserialize_transaction(data: str):
    try:
        transaction_data_dict = json.loads(json.loads(data))
        transaction = Transaction(**transaction_data_dict)
    except Exception as e:
        logger.error("Error deserializing: %s", e)
        transaction = None

    return transaction

def consume_from_kafka(topic):
    consumed_transactions = []

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='kafka:9092',
        group_id='my-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    try:
        for message in consumer:
            transaction_data = message.value
            try:
                transaction = deserialize_transaction(transaction_data)
                create_transaction_db(transaction)
                consumed_transactions.append({"partition": message.partition,
                                              "offset": message.offset,
                                              "key": message.key,
                                              "value": transaction_data})
            except Exception as e:
                logger.error("Error processing message: %s", e)

        consumer.close()
        return consumed_transactions
    except Exception as e:
        logger.error("Error consuming from Kafka: %s", e)
        raise
