from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = "VerifyLK"
    environment: str = Field(default="development")
    secret_key: str = Field(default="dev-secret-change", description="Use strong secret in production")
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7
    algorithm: str = "HS256"
    database_url: str = Field(default="sqlite:///./verifylk.db")
    s3_bucket: str | None = None
    s3_region: str | None = None
    email_from: str | None = None

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
