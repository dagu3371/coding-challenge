from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from app.database.models import Transaction
from app.database.db_utils import get_db

router = APIRouter()

@router.get("/transactions/{hash}")
def get_transaction_by_hash(hash: str, db: Session = Depends(get_db)):
    try:
        db_transaction = db.query(Transaction).filter_by(hash=hash).one()
        return db_transaction
    except NoResultFound:
        return {"error": "Transaction not found"}
