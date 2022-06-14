import datetime
from pydantic import Field
from beanie import Document, Link, Indexed, Replace, after_event

from . import BaseSchema, Address, SocialMedia
from .category_schema import Category
from .service_schema import Service

class WorkspaceProfile(BaseSchema):
    name: Indexed(str, unique=True) = Field(..., title="Name", description="Workspace unique name")
    description: str = Field(..., title="Description", description="Workspace work description")
    slogan: str | None = Field(None, title="Slogan", description="Workspace slogan")
    logo: str = Field(..., title="Logo", description="Workspace logo url")
    background_color: str | None = Field(None, title="Background", description="Workspace custom background")
    images: list[str] | None = Field([], title="Images", description="Workspace phisical place images")
    social_media: list[SocialMedia] | None = Field([], title="Social Media", description="Workspace social media")
    address: Address | None = Field(None, title="Address", description="Workspace address")
    
class Workspace(Document):
    category: Link[Category] = Field(..., title="Category", description="Workspace category")
    profile: WorkspaceProfile = Field(..., title="Profile", description="Workspace profile data")
    tags: list[str] | None = Field([], title="Tags", description="Workspace tags")
    services: list[Link[Service]] = Field(..., title="Services", description="Workspace enabled services")
    suscribers: list[str] = Field([]) # Change to users
    products: list[str] = Field([]) # Change to products
    notifications: list[str] = Field([]) # Change to notifications
    is_verified: bool = Field(False, title="Verification", description="Workspace verification")
    created_at: datetime.datetime | str = Field(datetime.datetime.now(), title="Created AT", description="Workspace creation date")
    updated_at: datetime.datetime | str = Field(datetime.datetime.now(), title="Updated AT", description="Workspace last update")
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "workspaces"
    
    class Settings:
        use_revision = True
        use_state_management = True
        validate_on_save = True
        use_cache = False # True