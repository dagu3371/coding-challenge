import logging
from app import db_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_transaction_db(transaction):
    logger.info("starting session")
    try:
        session = db_config.Session()
        session.add(transaction)
        session.commit()
        logger.info("Transaction created successfully.")
    except Exception as e:
        session.rollback()
        logger.info(transaction)
        logger.error("Error while creating transaction: %s", e)
    finally:
        session.close()
