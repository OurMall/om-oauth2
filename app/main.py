import datetime

from .app import create_application
from .database import init
from .common import Client, Permission
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

@app.on_event('startup')
async def on_startup():
    print("Server is starting...")
    await init()
    """client = Client(
        application_id="well-known-console-client",
        application_secret="1098306124",
        redirect_uris=["http://localhost:4201/callback", "http://localhost:4201/console"],
        application_type="web",
        contact="bcastro421@misena.edu.co",
        application_name="Our Mall for Developers",
        logo_uri="http://localhost:4201/assets/logos/om-logo.svg",
        application_uri="http://localhost:4201",
        policy_uri="http://localhost:4201/policy",
        tos_uri="http://localhost:4201/terms",
        subject_type="public",
        created_at=datetime.datetime.now()
    )
    await client.insert(skip_actions=['set_app_credentials'])"""

@app.on_event('shutdown')
async def on_shutdown():
    print("Shutdown application...")
    """await Client.find().delete_many()
    await Permission.find().delete_many()"""