from sqlalchemy import Column, Integer, String, Sequence, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, Sequence('transaction_id_seq'), primary_key=True)
    hash = Column(String(256), unique=True, index=True)
    fromAddress = Column(String(256))
    toAddress = Column(String(256))
    blockNumber = Column(BigInteger)
    executionTimestamp = Column(String(50))
    gasUsed = Column(Integer)
    gasCostInDollars = Column(BigInteger)
