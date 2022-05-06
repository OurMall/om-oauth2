import datetime
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from .core import settings
from .common import User, Permission, Group, Client

async def init():
    client = AsyncIOMotorClient(
        settings.MONGO_URI
    )
    database = client[settings.MONGO_DATABASE]
    await init_beanie(
        database=database,
        document_models=[
            User,
            Permission,
            Group,
            Client
        ]
    )

async def insert_base_models():
    console_client = Client(
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
        is_known=True,
        created_at=datetime.datetime.now()
    )
    await console_client.insert(skip_actions=['set_app_credentials'])
    base_permission = Permission(
        code_name="base",
        name="Base",
        description="Permiso base para todos los usuarios del sistema"
    )
    await base_permission.insert()
    client_user_group = Group(
        code_name="client",
        name="Cliente",
        description="Grupo de clientes que existen en la aplicación. También se toma como grupo/rol base",
        permissions=[base_permission]
    )
    await client_user_group.insert()
    

async def delete_base_models():
    await Client.find().delete_many()