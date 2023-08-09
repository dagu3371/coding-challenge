import pytest
from sqlalchemy.orm import Session
from app.database.db_config import engine, Session
from app.database.db_utils import create_tables

@pytest.fixture(autouse=True)
def setup_database():
    create_tables()
    yield

@pytest.fixture
def db() -> Session:
    connection = engine.connect()
    transaction = connection.begin()
    create_tables
    try:
        yield Session()
    finally:
        transaction.rollback()
        connection.close()
