import datetime
from beanie import Document, Link

from . import Address
from .category_schema import Category

class WorkspaceProfile(Document):
    name: str
    description: str
    slogan: str
    logo: str
    background_color: str
    images: list[str]
    social_media: list[str]
    address: Address
    
    class Collection:
        name = "workspacesProfiles"
    
    class Settings:
        validate_on_save = True

class Workspace(Document):
    category: Link[Category]
    profile: Link[WorkspaceProfile]
    tags: list[str]
    created_at: datetime.datetime | str
    updated_at: datetime.datetime | str
    
    class Collection:
        name = "workspaces"
    
    class Settings:
        validate_on_save = True
        use_cache = True
        cache_expiration_time = datetime.timedelta(minutes=5)
        cache_capacity = 5