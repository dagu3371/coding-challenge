from fastapi import APIRouter, BackgroundTasks
from app.kafka_utils.kafka_utils import consume_from_kafka

router = APIRouter()

@router.get("/consume-from-kafka/")
async def consume_from_kafka_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(consume_from_kafka, 'ethereum_transactions')
    return {"status": "Data is being consumed from Kafka in the background"}
