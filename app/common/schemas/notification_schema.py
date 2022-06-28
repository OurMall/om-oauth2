import datetime
from beanie import Document, Link
from pydantic import Field

from .user_schema import User

class Notification(Document):
    title: str = Field(..., title="Title", description="Notification title")
    description: str = Field(..., title="Description", description="Notification description")
    link: str = Field(None, title="Link", description="Notification link to navigate")
    to: list[Link[User]] = Field([], title="Objetive", description="Notification objetive or purpose subject")
    is_available: bool = Field(True, title="Status", description="Notification status")
    expired_at: int | datetime.datetime | None = Field(None, title="Expired AT", description="Notification expiration date")
    created_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Created AT", description="Notification created date")
    
    class Collection:
        name = "notifications"
    
    class Settings:
        use_state_management = True
        validate_on_save = True