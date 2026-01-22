import os
from dataclasses import dataclass


@dataclass
class Settings:
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    SERVICE_NAME: str = "Tasks Service"
    VERSION: str = "1.0.0"

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    DEBUG: bool = True

    # database settings
    DATABASE_URL: str = "postgresql://postgress:password@localhost:5432/trell_tasks"


def get_settings() -> Settings:
    return Settings(
        # API Settings
        API_V1_PREFIX=os.getenv("API_V1_PREFIX", "/api/v1"),
        SERVICE_NAME=os.getenv("SERVICE_NAME", "Tasks Service"),
        VERSION=os.getenv("VERSION", "1.0.0"),
        # Server Settings
        HOST=os.getenv("HOST", "0.0.0.0"),
        PORT=os.getenv("PORT", "8001"),
        DEBUG=os.getenv("DEBUG", "True"),
        # database settings
        DATABASE_URL=os.getenv(
            "DATABASE_URL", "postgresql://postgress:12345@localhost:5432/trell_tasks"
        ),
    )


settings = get_settings()
