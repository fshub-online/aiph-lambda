from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import List, Union
import logging

logger = logging.getLogger(__name__)


# Print environment file loading info before class definition
#print("Loading settings from environment variables...")
#env_file = ".env"
#try:
#    with open(env_file, "r") as f:
#        print(f"Contents of {env_file}:\n{f.read()}")
#except FileNotFoundError:
#    print(f"Environment file {env_file} not found.")

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    OAUTH2_SCHEME: str = "Bearer"
    OAUTH2_TOKEN_URL: str = "/api/v1/oauth/token"
    OAUTH2_JWT_URL: str = "/api/v1/oauth/jwt"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 60 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = "*"
    POSTGRES_HOST: str 
    POSTGRES_PORT: int 
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    LOGFIRE_WRITE_TOKEN: str
    LOGFIRE_ENVIRONMENT: str

    class Config:
        case_sensitive = True
        extra = "allow"
        env_file = ".env"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return v

    def assemble_db_connection(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Parse BACKEND_CORS_ORIGINS env var (comma-separated string)

    def get_cors_origins(self) -> List[str]:
        origins = self.BACKEND_CORS_ORIGINS
        if not origins:
            return ["*"]
        if isinstance(origins, str):
            return [o.strip() for o in origins.split(",") if o.strip()]
        return origins


settings = Settings()
