from pydantic import Field

from . import BaseModel

class Permission(BaseModel):
    code_name: str = Field(default=None)
    name: str = Field(default=None)
    description: str = Field(default=None)