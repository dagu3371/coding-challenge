from app.database.db_config import Session

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from app.database.models import Base
    from app.database.db_config import engine
    Base.metadata.create_all(bind=engine)
