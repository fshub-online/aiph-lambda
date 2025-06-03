import logfire
import logging
import os
import logging.config
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_v1_router
from app.db.session import engine, SessionLocal
import secrets
from app.schemas.user import UserCreate
from app.core.config import settings

# Configure logfire and logging as early as possible
logfire.configure(token=settings.LOGFIRE_WRITE_TOKEN, environment=settings.LOGFIRE_ENVIRONMENT)

LOGGING_CONFIG_FILE = "logging.conf"
if os.path.exists(LOGGING_CONFIG_FILE):
    logging.config.fileConfig(LOGGING_CONFIG_FILE, disable_existing_loggers=False)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().warning(
        f"Logging config file '{LOGGING_CONFIG_FILE}' not found. Using basicConfig."
    )

logfire.instrument_sqlalchemy(engine)
logfire.instrument_psycopg()


app = FastAPI(
    title="FastAPI backend for project Lambda",
    description="""
    This is a FastAPI backend for project Lambda.
    
    ## Docs
    - [Swagger UI](/api/v1/docs)
    - [ReDoc](/api/v1/redoc)
    - [OpenAPI JSON](/api/v1/openapi.json)
    """,
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    contact={
        "name": "Radek Zítek",
        "url": "https://www.fshub.online",
        "email": "radek.zitek@proton.me",
    },
)

logfire.instrument_fastapi(app, capture_headers=True)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# configure logfire
#instrument_all(app=app, engine=engine)

# connect to database and test if it works
@app.on_event("startup")
def startup_event():
    """
    Startup event to initialize the application.

    This function is called when the application starts.
    """
    with logfire.span("FastAPI startup"):
        # Add any startup tasks here, such as database connection
        try:
            from sqlalchemy import text, select
            from app.models.user import User
            from app.crud import crud_user
            # Test DB connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            # Check user count
            with SessionLocal() as session:
                result = session.execute(select(User))
                users = result.scalars().all()
                if len(users) == 0:
                    # Create default admin user
                    logfire.info("No users found in the database. Creating default admin user.")
                    password = secrets.token_urlsafe(16)
                    admin_user = UserCreate(
                        user_name="admin",
                        first_name="Admin",
                        last_name="User",
                        email="admin@fshub.online",
                        password=password
                    )
                    crud_user.create_user(session, user_in=admin_user)
                    logfire.info(f"Default admin user created. Username: admin, Password: {password}")
        except Exception as e:
            logfire.error(f"Database connection failed: {e}")
            raise

@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event to clean up resources.

    This function is called when the application shuts down.
    """
    with logfire.span("FastAPI shutdown"):
        # Add any shutdown tasks here, such as closing database connections
        pass

app.include_router(api_v1_router, prefix="/api/v1")

@app.get(
    "/", summary="Root endpoint", tags=["Root"], response_description="Welcome message"
)
def read_root():
    """
    Root endpoint for the FastAPI backend.

    Returns a welcome message.
    """
    return {"message": "Welcome to the FastAPI backend for project Lambda!"}

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.svg")
