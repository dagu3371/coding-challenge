from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import Transaction
from app.database.db_utils import get_db

router = APIRouter()

@router.get("/stats")
def get_transaction_by_hash(db: Session = Depends(get_db)):
    total_transactions = db.query(func.count(Transaction.id)).scalar()
    total_gas_used = db.query(func.sum(Transaction.gasUsed)).scalar()
    total_gas_cost_in_dollars = db.query(func.sum(Transaction.gasCostInDollars)).scalar()

    return {
        "totalTransactionsInDB": total_transactions,
        "totalGasUsed": total_gas_used,
        "totalGasCostInDollars": total_gas_cost_in_dollars
    }
