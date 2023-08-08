from app.db_config import Session

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from app.models import Base
    from app.db_config import engine
    Base.metadata.create_all(bind=engine)
