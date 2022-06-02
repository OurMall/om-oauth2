import datetime
from beanie import PydanticObjectId
from pydantic import Field

from . import BaseModel
from .permission_model import PermissionModel

class GroupCreate(BaseModel):
    code_name: str = Field(None)
    name: str = Field(None)
    description: str = Field(None)
    permissions: list[PermissionModel] = Field(None)

class GroupModel(GroupCreate):
    id: PydanticObjectId = Field(None)
    created_at: int | datetime.datetime = Field(None)
    updated_at: int | datetime.datetime = Field(None)