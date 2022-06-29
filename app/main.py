from socketio import ASGIApp
from fastapi.middleware.cors import CORSMiddleware

from .app import create_application
from .io import create_sio
from .core import database, settings
from .common import Client
from .modules.search import search_engine
from .modules.oauth2 import oauth2
from .modules.connect import connect
from .modules.user import user
from .modules.workspace import workspace
from .modules.category import category
from .modules.service import service
from .modules.workspace.product import product
from .modules.workspace.post import post
from .modules.file import file

app = create_application()

app.include_router(
    router=search_engine.router,
    tags=["Search methods"]
)

app.include_router(
    router=oauth2.router,
    tags=["OAuth2 Protocol"]
)

app.include_router(
    router=connect.router,
    tags=["Open ID Connect"]
)

app.include_router(
    router=user.router,
    tags=["User Endpoints"]
)

app.include_router(
    router=workspace.router,
    tags=["Workspaces"]
)

app.include_router(
    router=product.router,
    tags=["Products"]
)

app.include_router(
    router=post.router,
    tags=["Posts"]
)

app.include_router(
    router=category.router,
    tags=["Categories"]
)

app.include_router(
    router=service.router,
    tags=["Services"]
)

app.include_router(
    router=file.router,
    tags=["Files"]
)

@app.on_event("startup")
async def on_startup():
    print("Server is starting: Production: {0}".format(settings.PRODUCTION))
    await database.init()
    #await database.insert_base_models()
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=[origin.application_uri for origin in await Client.find().to_list()],
        allow_methods=["*"],
        allow_headers=["*"]
    )

@app.on_event("shutdown")
async def on_shutdown():
    print("Shutdown application...")
    #await database.delete_base_models()

sio = create_sio()

io_app = ASGIApp(
    socketio_server=sio,
    other_asgi_app=app
)