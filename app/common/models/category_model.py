import datetime
from pydantic import Field

from . import BaseModel

class CategoryCreate(BaseModel):
    name: str = Field(..., title="Name", description="Category unique name")
    description: str = Field(..., max_length=300, title="Description", description="Description for category")

class CategoryModel(CategoryCreate):
    id: object
    created_at: datetime.datetime | str
    updated_at: datetime.datetime | str