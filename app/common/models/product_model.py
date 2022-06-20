import datetime
from beanie import PydanticObjectId
from pydantic import Field

from app.common.schemas import Price, ProductStatus

from . import BaseModel

class ProductCreate(BaseModel):
    name: str = Field(None)
    detail: str = Field(None)
    price: Price = Field(None)
    stock: int = Field(None)
    images: list[str] = Field(None)
    status: ProductStatus = Field(None)
    is_available: bool = Field(None)
    workspace: str = Field(None)

class ProductModel(ProductCreate):
    id: PydanticObjectId = Field(None)
    vat: int = Field(None)
    created_at: int | datetime.datetime = Field(None)
    updated_at: int | datetime.datetime = Field(None)