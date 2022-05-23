import datetime
from pydantic import Field
from beanie import Document, Link, Indexed, Replace, after_event

from . import Address, SocialMedia
from .category_schema import Category

class WorkspaceProfile(Document):
    name: Indexed(str, unique=True)
    description: str
    slogan: str
    logo: str
    background_color: str
    images: list[str]
    social_media: list[SocialMedia]
    address: Address
    
    class Collection:
        name = "workspacesProfiles"
    
    class Settings:
        validate_on_save = True

class Workspace(Document):
    category: Link[Category]
    profile: Link[WorkspaceProfile]
    tags: list[str]
    services: list[str] # Change to services
    suscribers: list[str] # Change to users
    products: list[str] # Change to products
    notifications: list[str] # Change to notifications
    is_verified: bool = Field(False, title="Verification", description="Workspace verification")
    created_at: datetime.datetime | str = Field(datetime.datetime.now(), title="Created AT", description="Workspace creation date")
    updated_at: datetime.datetime | str = Field(datetime.datetime.now(), title="Updated AT", description="Workspace last update")
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "workspaces"
    
    class Settings:
        use_revision = True # This feature helps to avoid losses of data
        use_state_management = True # Save only changed documents
        validate_on_save = True # Validate data before save
        use_cache = True
        cache_expiration_time = datetime.timedelta(minutes=5)
        cache_capacity = 5