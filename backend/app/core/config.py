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

    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    PGADMIN_DEFAULT_EMAIL: Optional[EmailStr] = None
    PGADMIN_DEFAULT_PASSWORD: Optional[str] = None

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
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
