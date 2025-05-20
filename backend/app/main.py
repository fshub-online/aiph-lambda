import logfire
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_v1_router
from app.db.session import engine, SessionLocal
import secrets
from app.schemas.user import UserCreate
from app.core.logfire_instance import instrument_all
from app.core.config import settings

app = FastAPI(
    title="FastAPI backend for project Lambda",
    description="""
    This is a FastAPI backend for project Lambda.
    
    ## Features
    - User authentication (OAuth2, JWT)
    - User CRUD operations
    - Healthcheck endpoint
    - PostgreSQL database integration
    - Modular API versioning
    
    ## Docs
    - [Swagger UI](/api/v1/docs)
    - [ReDoc](/api/v1/redoc)
    
    ## Contact
    - Name: Radek Zítek
    - Website: https://www.fshub.online
    - Email: radek.zitek@proton.me
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



# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# configure logfire
instrument_all(app=app, engine=engine)

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
