import logfire
import logging
from app.core.config import settings

# configure logfire
logfire.configure(
    token=settings.LOGFIRE_WRITE_TOKEN, console=False, inspect_arguments=False
)

logfire.instrument_pydantic()


# Instrumentation for FastAPI, psycopg, asyncpg, and SQLAlchemy should be called in main.py after app/engine are created.
# To allow import order flexibility, expose instrument functions here for use in main.py:
def instrument_all(app=None, engine=None):
    logfire.instrument_fastapi(app, capture_headers=True)
    logfire.instrument_psycopg()
    logfire.instrument_asyncpg()
    if engine is not None:
        logfire.instrument_sqlalchemy(engine=engine)


logfire_instance = logfire

# Set up logging from config file
logging.config.fileConfig(
    "app/logging.conf",
    disable_existing_loggers=True,
)
