from fastapi.middleware.cors import CORSMiddleware

from .app import create_application
from .database import init, insert_base_models, delete_base_models
from .common import Client
from .modules.oauth2 import oauth2
from .modules.connect import connect

app = create_application()

app.include_router(
    router=oauth2.router,
    tags=["OAuth2 Protocol"]
)

app.include_router(
    router=connect.router,
    tags=["Open ID Connect"]
)

@app.on_event("startup")
async def on_startup():
    print("Server is starting...")
    await init()
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=[origin.application_uri for origin in await Client.find().to_list()],
        allow_methods=["*"],
        allow_headers=["*"]
    )
    #await insert_base_models()

@app.on_event("shutdown")
async def on_shutdown():
    print("Shutdown application...")
    #await delete_base_models()