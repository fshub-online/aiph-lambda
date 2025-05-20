from fastapi import FastAPI
from app.api.v1 import api_v1_router

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
        "email": "radek.zitek@proton.me"
    }
)

app.include_router(api_v1_router, prefix="/api/v1")

@app.get("/", summary="Root endpoint", tags=["Root"], response_description="Welcome message")
def read_root():
    """
    Root endpoint for the FastAPI backend.
    
    Returns a welcome message.
    """
    return {"message": "Welcome to the FastAPI backend for project Lambda!"}