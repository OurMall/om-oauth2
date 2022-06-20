import datetime
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from . import settings

from app.common import (
    User, 
    Permission, 
    Group, 
    Client, 
    Category, 
    Workspace, 
    Service,
    Product
)

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
            Client,
            Category,
            Workspace,
            Service,
            Product
        ]
    )

async def insert_base_models():
    await _create_init_services()
    await _create_init_clients()
    await _create_init_roles()
    await _create_init_categories()

async def delete_base_models():
    await Client.find().delete_many()
    await Group.find().delete_many()
    await Permission.find().delete_many()
    await User.find().delete_many()

async def _create_init_clients():
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
    client = Client(
        application_id="well-known-client",
        application_secret="03072004",
        redirect_uris=["http://localhost:4200/callback", "http://localhost:4200/console"],
        application_type="web",
        contact="bcastro421@misena.edu.co",
        application_name="Our Mall",
        logo_uri="http://localhost:4200/assets/logos/om-logo.svg",
        application_uri="http://localhost:4200",
        policy_uri="http://localhost:4200/policy",
        tos_uri="http://localhost:4200/terms",
        subject_type="public",
        is_known=True,
        created_at=datetime.datetime.now()
    )
    await client.insert(skip_actions=['set_app_credentials'])
    production_client = Client(
        application_id="well-known-client-production",
        application_secret="74807f0f24780b21aec0320a53593ebf9f8b08d4",
        redirect_uris=["https://ourmall.azurewebsites.net/callback", "https://ourmall.azurewebsites.net"],
        application_type="web",
        contact="bcastro421@misena.edu.co",
        application_name="Our Mall",
        logo_uri="https://ourmall.azurewebsites.net/assets/logos/om-logo.svg",
        application_uri="https://ourmall.azurewebsites.net",
        policy_uri="https://ourmall.azurewebsites.net/policy",
        tos_uri="https://ourmall.azurewebsites.net/terms",
        subject_type="public",
        is_known=True,
        created_at=datetime.datetime.now()
    )
    await production_client.insert(skip_actions=['set_app_credentials'])

async def _create_init_roles() -> None:
    base_permission = Permission(
        code_name="base",
        name="Base",
        description="Permiso base para todos los usuarios del sistema"
    )
    await base_permission.insert()
    client = Group(
        code_name="client",
        name="Cliente",
        description="Grupo de clientes que existen en la aplicación. También se toma como grupo/rol base",
        permissions=[base_permission]
    )
    seller = Group(
        code_name="seller",
        name="Vendedor",
        description="Grupo de vendedores que existen en la aplicación.",
        permissions=[base_permission]
    )
    await Group.insert_many([client, seller])

async def _create_init_services() -> None:
    notifications = Service(
        code_name="notifications",
        name="Notificaciones",
        description="Publica notificaciones en tu espacio de trabajo para todos los suscriptores del mismo",
        activate=True
    )
    products = Service(
        code_name="products",
        name="Inventario de productos",
        description="Gestiona los productos que manejes y muestralos al público",
        activate=True
    )
    cash_register = Service(
        code_name="cash_register",
        name="Sistema de caja",
        description="Gestiona tus ventas diarias y genera facturas",
        activate=False
    )
    sales = Service(
        code_name="sales",
        name="Ventas en línea",
        description="Vende tus productos en línea y recibe el dinero por la compra",
        activate=False
    )
    await Service.insert_many([
        notifications,
        products,
        cash_register,
        sales
    ])

async def _create_init_categories():
    food = Category(
        code_name="food",
        name="Comidas",
        description="Todo lo relacionado a comidas"
    )
    clothes = Category(
        code_name="clothes",
        name="Ropa",
        description="Todo lo relacionado con ropa"
    )
    await Category.insert_many([
        food, clothes
    ])