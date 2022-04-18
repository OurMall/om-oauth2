from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.core import settings

"""
    :class AsyncMongoDBClient - Class for getting db's & collections from
    MongoDB
"""
class AsyncMongoDBClient:
    
    """
        :property db - Get the default database for use a collection set.
    """
    @property
    def db(self) -> AsyncIOMotorDatabase:
        return self._get_database()
    
    """
        :method __init__
        :params connection_uri - URI for connect to the MongoDB.
    """   
    def __init__(self, connection_uri: str | None) -> None:
        if connection_uri is None:
            self._client = AsyncIOMotorClient(settings.MONGO_URI)
        else:
            self._client = AsyncIOMotorClient(connection_uri)
    
    """
        :method _get_database - Obtain the specified database.
    """
    def _get_database(self, name: str=settings.MONGO_DATABASE) -> AsyncIOMotorDatabase:
        return self._client[name]
    
    """
        :method use_collection - Obtain the specified collection.
    """
    def get_collection(self, name: str) -> AsyncIOMotorCollection:
        collection: AsyncIOMotorCollection = self.db[name]
        return collection

async_mongodb_client = AsyncMongoDBClient()