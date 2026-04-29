from app.core.config import settings
from app.models.models import Event
from beanie import init_beanie
from pymongo import AsyncMongoClient


async def connect_to_mongo():
    print("connecting to mongodb ...")

    client = AsyncMongoClient(settings.MONGODB_URL)
    database = client[settings.DATABASE_NAME]

    await init_beanie(database=database, document_models=[Event])

    print("connected to mongodb ...")


async def close_mongo_connection():
    print("c,ose mongo connection")
