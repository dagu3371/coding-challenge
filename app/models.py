from pydantic import BaseModel

class Transaction(BaseModel):
    hash: str
    fromAddress: str
    toAddress: str
    blockNumber: str
    executionTimestamp: str
    gasUsed: int
    gasCostInDollars: int
