from fastapi import APIRouter, BackgroundTasks
from kafka import KafkaProducer
from app.data_utils.data_utils import produce_data_to_kafka
from app.database.db_utils import create_tables

router = APIRouter()

@router.get("/produce-to-kafka/")
async def produce_to_kafka_endpoint(background_tasks: BackgroundTasks):
    create_tables()
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    background_tasks.add_task(produce_data_to_kafka, producer)
    return {"status": "Data is being produced to Kafka in the background"}
