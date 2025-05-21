from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.logfire_instance import logfire

SQLALCHEMY_DATABASE_URL = settings.assemble_db_connection()

logfire.info(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

# Create a sync engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)