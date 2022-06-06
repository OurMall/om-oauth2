from socketio import ASGIApp
from fastapi.middleware.cors import CORSMiddleware

from .app import create_application
from .io import create_sio
from .core import database, settings
from .common import Client
from .modules.oauth2 import oauth2
from .modules.connect import connect
from .modules.user import user
from .modules.workspace import workspace
from .modules.category import category
from .modules.service import service
from .namespaces import NotificationNamespace

app = create_application()

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
    router=category.router,
    tags=["Categories"]
)

app.include_router(
    router=service.router,
    tags=["Services"]
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

sio.register_namespace(
    namespace_handler=NotificationNamespace("/notification")
)

io_app = ASGIApp(
    socketio_server=sio,
    other_asgi_app=app
)