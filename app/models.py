from pydantic import BaseModel
# from typing import Optional

class Transaction(BaseModel):
    hash: str
    fromAddress: str
    toAddress: str
    blockNumber: str
    executionTimestamp: str
    # executedAt: str
    # gasUsed: str
    # gasCostInDollars: str
