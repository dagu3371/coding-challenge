from app.models import Transaction

def test_transaction_model():
    data = {
            "hash": "0x4bcb4c8de18d4da5db5e713d8caf34897497cb0579dd6b233881bf5d60fa956c",
            "fromAddress": "0x065e3dbafcb2c26a978720f9eb4bce6ad9d644a1",
            "toAddress": "0xa69babef1ca67a37ffaf7a485dfff3382056e78c",
            "blockNumber": "17818542",
            "executionTimestamp": "2023-08-01T07:05:59",
            "gasUsed": 110059,
            "gasCostInDollars": 3884936354412928
    }

    transaction = Transaction(**data)
    assert transaction.hash == "0x4bcb4c8de18d4da5db5e713d8caf34897497cb0579dd6b233881bf5d60fa956c"
    assert transaction.fromAddress == "0x065e3dbafcb2c26a978720f9eb4bce6ad9d644a1"
    assert transaction.toAddress == "0xa69babef1ca67a37ffaf7a485dfff3382056e78c"
    assert transaction.blockNumber == "17818542"
    assert transaction.executionTimestamp == "2023-08-01T07:05:59"
    assert transaction.gasUsed == 110059
    assert transaction.gasCostInDollars == 3884936354412928
