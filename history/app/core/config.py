from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME = "History Service"
    VERSION = "1.0"

    HOST: str = "0.0.0.0"
    PORT: int = 8003
    DEBUG: bool = True

    DATABASE_NAME: str = "trello_hisotry"
    MONGODB_URL: str = "mongodb://mongo:27017"

    CELERY_BACKEND: str = "redis://redis:6379/0"
    RABBITMQ_URL: str = "ampq://guest:guest@rabbitmq:5672/"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
