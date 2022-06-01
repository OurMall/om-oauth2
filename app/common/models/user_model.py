import datetime
from pydantic import Field, validator

from app.common import Address, Profile

from . import BaseModel, PyObjectId
from .permission_model import Permission
from .group_model import Group
from .client_model import ClientModel

from app.common import Gender

class UserLogin(BaseModel):
    email: str = Field(..., title="Email", description="User unique email address")
    password: str = Field(..., title="Password", description="User password for credentials")
    
class UserSignup(UserLogin):
    given_name: str = Field(..., title="Given Name", description="User given name")
    family_name: str = Field(..., title="Family Name", description="User lastname or family name")
    gender: Gender = Field(..., title="Gender", description="User gender")
    phone_number: str = Field(..., title="Phone Number", description="User phone number")
    birthdate: datetime.datetime | str = Field(..., title="Birthdate", description="User birthdate")
    profile: Profile | None = Field(None, title="Profile", description="User profile information")
    middle_name: str | None = Field(None, title="Middle Name", description="User middle name")
    zoneinfo: str | None = Field(None, title="Zoneinfo", description="User zoneinfo description")
    locale: str | None = Field(None, title="Locale", description="User locale language")

class UserModel(UserSignup):
    id: PyObjectId = Field(default_factory=PyObjectId)
    workspaces: list[object]

class UserPartialUpdate(BaseModel):
    given_name: str | None
    family_name: str | None
    middle_name: str | None
    phone_number: str | None
    Profile: Profile | None
    address: Address | None