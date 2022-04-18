from .app import create_application
from .core import async_mongodb_client

app = create_application()

@app.on_event('startup')
async def on_startup():
    print("Server is starting...")
    async with async_mongodb_client.get_collection("clients_origins") as origins:
        pass

@app.on_event('shuwtdown')
async def on_shutdown():
    print("Shutdown application")