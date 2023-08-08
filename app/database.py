from app import db_config

def create_transaction_db(transaction):
    try:
        session = db_config.Session()
        session.add(transaction)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
