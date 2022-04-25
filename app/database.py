from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .core import settings
from .common import User, Permission, Group, Client

async def init():
    client = AsyncIOMotorClient(
        settings.MONGO_URI
    )
    database = client[settings.MONGO_DATABASE]
    print(settings.MONGO_URI, settings.MONGO_DATABASE)
    await init_beanie(
        database=database,
        document_models=[
            User,
            Permission,
            Group,
            Client
        ]
    )