from fastapi import FastAPI
from app.endpoints.produce_to_kafka import router as produce_to_kafka_router
from app.endpoints.consume_from_kafka import router as consume_from_kafka_router
from app.endpoints.transactions import router as transactions_router
from app.endpoints.stats import router as stats_router
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(produce_to_kafka_router)
app.include_router(consume_from_kafka_router)
app.include_router(transactions_router)
app.include_router(stats_router)
