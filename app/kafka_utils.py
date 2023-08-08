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

def consume_from_kafka(topic, num_messages=10):
    consumed_transactions = []

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='kafka:9092',
        group_id='my-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )
    logger.info(consumer)
    try:
        for _ in range(num_messages):
            message = next(consumer)
            logger.info("Received kafka message: %s", message)
            transaction_data = message.value
            logger.info("Received transaction data: %s", transaction_data)
            try:
                logger.info('desserializing')
                transaction = deserialize_transaction(transaction_data)
                logger.info('uhhh')
                logger.info(transaction)
                create_transaction_db(transaction)
                consumed_transactions.append({"partition": message.partition,
                                              "offset": message.offset,
                                              "key": message.key,
                                              "value": transaction_data})
                logger.info(consumed_transactions)
            except Exception as e:
                logger.error("Error processing message: %s", e)

    except Exception as e:
        logger.error("Error consuming from Kafka: %s", e)
        raise
    consumer.close()
    logger.info('Finished')
    logger.info(consumed_transactions)
    return consumed_transactions
