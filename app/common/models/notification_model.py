import datetime
from pydantic import Field

from . import BaseModel

class NotificationCreate(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    link: str = Field(None)
    to: list[str] = Field([])
    is_available: bool = Field(True)
    expired_at: int | datetime.datetime = Field(None)

class NotificationModel(NotificationCreate):
    created_at: int | datetime.datetime = Field(None)