import datetime
from pydantic import Field, validator

from app.common import Address, Profile

from . import BaseModel
from .permission_model import Permission
from .group_model import Group
from .client_model import ClientModel

from app.common import Gender

class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    
class UserSignup(UserLogin):
    given_name: str = Field(...)
    family_name: str = Field(...)
    middle_name: str | None = Field(None)
    gender: Gender = Field(...)
    phone_number: str = Field(...)
    birthdate: datetime.datetime | str = Field(...)
    zoneinfo: str | None = Field(None)
    locale: str | None = Field(None)

class UserModel(UserSignup):
    pass

class UserPartialUpdate(BaseModel):
    given_name: str | None
    family_name: str | None
    middle_name: str | None
    phone_number: str | None
    Profile: Profile | None
    address: Address | None
    