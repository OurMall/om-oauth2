import datetime
from beanie import PydanticObjectId
from pydantic import Field

from app.common import Address, SocialMedia

from . import BaseModel
from .service_model import ServiceModel
from .category_model import CategoryModel
from .product_model import ProductModel
from .post_model import PostModel

class WorkspaceProfileModel(BaseModel):
    name: str = Field(None)
    description: str = Field(None)
    slogan: str = Field(None)
    logo: str = Field(None)
    background_color: str = Field(None)
    images: list[str] = Field([])
    social_media: list[SocialMedia] = Field([])
    address: Address = Field(None)

class WorkspaceCreate(BaseModel):
    category: CategoryModel = Field(None)
    profile: WorkspaceProfileModel = Field(None)
    services: list[str] = Field([])
    tags: list[str] = Field([])
    #owner: str = Field(None)

class WorkspaceModel(WorkspaceCreate):
    id: PydanticObjectId = Field(None)
    is_verified: bool = Field(None)
    services: list[ServiceModel] = Field([])
    suscribers: list[str] = Field([])
    products: list[ProductModel] = Field([])
    posts: list[PostModel] = Field([])
    created_at: int | datetime.datetime = Field(None)
    updated_at: int | datetime.datetime = Field(None)