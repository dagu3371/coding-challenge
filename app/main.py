from fastapi import FastAPI, BackgroundTasks, Depends
from kafka import KafkaProducer
from .kafka_utils import consume_from_kafka
from .data_utils import produce_data_to_kafka
from app.models import Transaction
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from app.db_utils import get_db, create_tables
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/produce-to-kafka/")
async def produce_to_kafka_endpoint(background_tasks: BackgroundTasks):
    create_tables()
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    background_tasks.add_task(produce_data_to_kafka, producer)
    return {"status": "Data is being produced to Kafka in the background"}

@app.get("/consume-from-kafka/")
async def consume_from_kafka_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(consume_from_kafka, 'ethereum_transactions')
    return {"status": "Data is being consumed from Kafka in the background"}

@app.get("/transactions/{hash}")
def get_transaction_by_hash(hash: str, db: Session = Depends(get_db)):
    try:
        db_transaction = db.query(Transaction).filter_by(hash=hash).one()
        return db_transaction
    except NoResultFound:
        return {"error": "Transaction not found"}

@app.get("/stats")
def get_transaction_by_hash(db: Session = Depends(get_db)):
    total_transactions = db.query(func.count(Transaction.id)).scalar()
    total_gas_used = db.query(func.sum(Transaction.gasUsed)).scalar()
    total_gas_cost_in_dollars = db.query(func.sum(Transaction.gasCostInDollars)).scalar()

    return {
        "totalTransactionsInDB": total_transactions,
        "totalGasUsed": total_gas_used,
        "totalGasCostInDollars": total_gas_cost_in_dollars
    }