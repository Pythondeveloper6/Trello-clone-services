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
    MONGODB_URL: str = "mongodb://localhost:27017"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
