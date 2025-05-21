from typing import Generator
from app.db.session import SessionLocal
from app.api.v1.endpoints.oauth import read_users_me



def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_active_user():
    """
    Dependency to get the current authenticated user.
    """
    return read_users_me