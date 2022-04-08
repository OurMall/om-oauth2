from pydantic import Field

from . import BaseModel
from .permission_model import Permission

class Group(BaseModel):
    code_name: str = Field(default=None)
    name: str = Field(default=None)
    description: str = Field(default=None)
    permissions: list[Permission] = Field(default=None)