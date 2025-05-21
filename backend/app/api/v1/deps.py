from typing import Generator
from app.db.session import SessionLocal



def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# def get_current_active_user():
#     """
#     Dependency to get the current authenticated user.
#     """
#     return read_users_me