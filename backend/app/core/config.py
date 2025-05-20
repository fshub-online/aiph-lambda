from pydantic import EmailStr, field_validator
from pydantic_settings import BaseSettings
from typing import Optional, List, Union

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    OAUTH2_SCHEME: str = "Bearer"
    OAUTH2_TOKEN_URL: str = "/api/v1/oauth/token"
    OAUTH2_JWT_URL: str = "/api/v1/oauth/jwt"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    SERVER_NAME: Optional[str] = None
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = "*"

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "postgres"
    PG_DB: str = "db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    PGADMIN_DEFAULT_EMAIL: Optional[EmailStr] = None
    PGADMIN_DEFAULT_PASSWORD: Optional[str] = None

    LOGFIRE_WRITE_TOKEN: Optional[str] = None

    class Config:
        case_sensitive = True
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
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        return f"postgresql://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


    # Parse BACKEND_CORS_ORIGINS env var (comma-separated string)
    def get_cors_origins(self) -> List[str]:
        origins = self.BACKEND_CORS_ORIGINS
        if not origins:
            return ["*"]
        if isinstance(origins, str):
            return [o.strip() for o in origins.split(",") if o.strip()]
        return origins

settings = Settings()
