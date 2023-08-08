from fastapi import FastAPI, BackgroundTasks
from kafka import KafkaProducer
from .kafka_utils import consume_from_kafka
from .data_utils import produce_data_to_kafka

app = FastAPI()

@app.get("/produce-to-kafka/")
async def produce_to_kafka_endpoint(background_tasks: BackgroundTasks):
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    background_tasks.add_task(produce_data_to_kafka, producer)
    return {"status": "Data is being produced to Kafka in the background"}

@app.get("/consume-from-kafka/")
def consume_from_kafka_endpoint():
    messages = consume_from_kafka('ethereum_transactions', num_messages=10)
    return {"messages": messages}
