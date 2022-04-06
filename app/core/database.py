from motor.motor_asyncio import AsyncIOMotorClient

def create_async_client() -> AsyncIOMotorClient:
    try:
        client = AsyncIOMotorClient()
    except Exception as e:
        raise Exception
    else:
        return client