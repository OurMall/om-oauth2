import datetime
from typing import Any
from pydantic import Field

from . import BaseModel

class ServiceCreate(BaseModel):
    code_name: str = Field(..., title="Code Name", description="Service code name")
    name: str = Field(..., title="Name", description="Service name")
    description: str = Field(..., title="Description", description="Service description")
    activate: bool = Field(False, title="Activation", description="Service activation type")

class ServiceModel(ServiceCreate):
    id: Any
    created_at: datetime.datetime
    updated_at: datetime.datetime