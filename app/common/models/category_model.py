import datetime
from beanie import PydanticObjectId
from pydantic import Field

from . import BaseModel

class CategoryCreate(BaseModel):
    code_name: str = Field(None)
    name: str = Field(None)
    description: str = Field(None)

class CategoryModel(CategoryCreate):
    id: PydanticObjectId = Field(None)
    created_at: int | datetime.datetime = Field(None)
    updated_at: int | datetime.datetime = Field(None)