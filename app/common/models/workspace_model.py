from . import BaseModel

from app.common import Address, SocialMedia

class WorkspaceProfileModel(BaseModel):
    name: str
    description: str
    slogan: str | None
    logo: str
    background_color: str | None
    images: list[str] | None
    social_media: list[SocialMedia] | None
    address: Address | None

class WorkspaceCreate(BaseModel):
    category: str
    profile: WorkspaceProfileModel
    services: list[str]
    tags: list[str] | None
    owner: str | None

class WorkspaceModel(BaseModel):
    pass