from typing import Generator
from app.db.session import SessionLocal
import logging

logger = logging.getLogger(__name__)



def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
