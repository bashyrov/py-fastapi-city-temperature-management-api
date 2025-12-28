from sqlalchemy.orm import Session
from database.engine import SessionLocal

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()