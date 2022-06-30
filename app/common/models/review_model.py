import datetime
from beanie import PydanticObjectId
from pydantic import Field

from . import BaseModel

class ReviewModel(BaseModel):
    id: PydanticObjectId = Field(None)
    user_id: str = Field(None)
    comment: str = Field(None)
    created_at: int | datetime.datetime = Field(None)