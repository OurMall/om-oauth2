import enum
import datetime
from pydantic import Field
from beanie import (
    Document, 
    Link, 
    Insert, 
    Replace, 
    Indexed,
    before_event,
    after_event,
)

from . import BaseSchema, Address
from .permission_schema import Permission
from .group_schema import Group
from .client_schema import Client
from .workspace_schema import Workspace

class Gender(enum.Enum):
    MALE="male"
    FEMALE="female"
    OTHER="other"

class Profile(BaseSchema):
    picture: str = Field(..., title="Picture", description="User profile picture")
    website: str | None = Field(None, title="Website", description="User social media")
    biography: str | None = Field(None, title="Biography", description="User biography or life description")

class User(Document):
    name: str | None = Field(None, title="Name", description="User complete name")
    given_name: str = Field(..., title="Given Name", description="User given name")
    family_name: str = Field(..., title="Family Name", description="User family name")
    middle_name: str | None = Field(None, title="Middle Name", description="User middle name")
    nickname: str | None = Field(None, title="Nickname", description="User nickname")
    preferred_username: str | None = Field(None, title="Preferred Nickname", description="User preferred nickname")
    gender: Gender = Field(..., title="Gender", description="User gender")
    email: Indexed(str) = Field(..., title="Email", description="User unique email address")
    password: str | None = Field(None, title="Password", description="User password")
    phone_number: str = Field(..., title="Phone Number", description="User phone number")
    profile: Profile | None = Field(None, title="Profile", description="User profile information")
    address: Address | None = Field(None, title="Address", description="User address information")
    birthdate: datetime.datetime | str = Field(..., title="Birthdate", description="User birthdate")
    zoneinfo: str | None = Field(None, title="Zoneinfo", description="User zoneinfo")
    locale: str | None = Field(None, title="Locale", description="User locale information language")
    email_verified: bool = Field(False, title="Email Verified", description="User account status")
    phone_number_verified: bool = Field(False, title="Phone Number Verified", description="User phone number status")
    is_blocked: bool = Field(False, title="Blocked", description="User account status on the app")
    is_disabled: bool = Field(False, title="Disabled", description="Account status")
    created_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Created AT", description="User created account date")
    updated_at: int | datetime.datetime = Field(datetime.datetime.now(), title="Updated AT", description="User last updated")
    workspaces: list[Link[Workspace]] = Field([], title="Workspaces", description="User created workspaces")
    groups: list[Link[Group]] = Field([], title="Groups", description="User groups or roles")
    permissions: list[Link[Permission]] = Field([], title="Permissions", description="User permissions")
    #clients: list[Link[Client]] = Field([])
    #favorites: list[Link[Product]] = Field([])
    #rooms: list[Link[Room]] = Field([])
    
    @before_event(Insert)
    def join_fullname(self):
        self.name = f"{self.given_name.strip()}{self.middle_name.strip() if self.middle_name else ' '}{self.family_name.strip()}"
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "users"
    
    class Settings:
        #use_revision = True
        use_state_management = True
        validate_on_save = True
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=60)
        cache_capacity = 3