import datetime
from beanie import PydanticObjectId
from pydantic import Field

from . import BaseModel

class PostCreate(BaseModel):
    title: str = Field(None)
    content: str = Field(None)
    workspace: str = Field(None)
    image: str = Field(None)
    is_public: bool = Field(True)

class PostModel(PostCreate):
    id: PydanticObjectId = Field(None)
    created_at: int | datetime.datetime = Field(None)
    updated_at: int | datetime.datetime = Field(None)