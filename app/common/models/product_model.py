import datetime
from beanie import PydanticObjectId
from pydantic import Field

from app.common.schemas import Price, ProductStatus

from . import BaseModel

class ProductCreate(BaseModel):
    name: str = Field(...)
    detail: str = Field(...)
    price: Price = Field(...)
    stock: int = Field(...)
    images: list[str] = Field(...)
    status: ProductStatus = Field(...)
    is_available: bool = Field(...)

class ProductModel(ProductCreate):
    id: PydanticObjectId = Field(None)
    vat: int = Field(None)
    created_at: int | datetime.datetime = Field(None)
    updated_at: int | datetime.datetime = Field(None)