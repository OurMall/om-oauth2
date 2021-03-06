import datetime
from beanie import PydanticObjectId
from pydantic import Field

from app.common import Address, Profile

from . import BaseModel
from .permission_model import PermissionModel
from .group_model import GroupModel
from .client_model import ClientModel
from .workspace_model import WorkspaceModel

from app.common import Gender

class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    
class UserSignup(UserLogin):
    given_name: str = Field(...)
    family_name: str = Field(...)
    gender: Gender = Field(...)
    phone_number: str = Field(...)
    profile: Profile | None = Field(None)
    birthdate: datetime.datetime | str = Field(...)
    zoneinfo: str | None = Field(None)
    locale: str | None = Field(None)

class UserModel(UserSignup):
    id: PydanticObjectId = Field(...)
    name: str = Field(...)
    middle_name: str | None = Field(None)
    nickname: str | None = Field(None)
    preferred_username: str | None = Field(None)
    address: Address | None = Field(None)
    email_verified: bool = Field(False)
    phone_number_verified: bool = Field(False)
    is_blocked: bool = Field(False)
    is_disabled: bool = Field(False)
    created_at: datetime.datetime | None = Field(None)
    updated_at: datetime.datetime | None = Field(None)
    workspaces: list[WorkspaceModel] = Field([])
    groups: list[GroupModel] = Field([])
    permissions: list[PermissionModel] = Field([])

class UserPartialUpdate(BaseModel):
    given_name: str | None = Field(None)
    family_name: str | None = Field(None)
    middle_name: str | None = Field(None)
    nickname: str | None = Field(None)
    phone_number: str | None = Field(None)
    profile: Profile | None = Field(None)
    address: Address | None = Field(None)
    email_verified: bool | None = Field(None)
    phone_number_verified: bool | None = Field(None)
    is_disabled: bool | None = Field(None)

class UserResetPassword(BaseModel):
    token: str = Field(..., title="Token", description="Token provided by email")
    new_password: str = Field(..., title="New password", description="New password to set in DB", min_length=8)
    confirm_password: str = Field(..., title="Confirm Password", description="Confirm password repeated for verify", min_length=8)