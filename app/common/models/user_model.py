import datetime
from pydantic import Field, validator

from . import BaseModel
from .profile_model import Profile
from .permission_model import Permission
from .group_model import Group

class User(BaseModel):
    uid: str|bytes = Field(default=None)
    name: str = Field(default=None)
    last_name: str = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)
    profile: Profile = Field(default=None) # Pending
    groups: list[Group] = Field(default=None) # Pending
    permissions: list[Permission] = Field(default=None) # Pending
    accept_terms: bool = Field(default=None)
    is_verify: bool = Field(default=False)
    is_disabled: bool = Field(default=False)
    is_blocked: bool = Field(default=False)
    birthday: datetime.datetime = Field(default=None)
    created_at: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    @validator("email")
    def valid_email(cls, value: str):
        if not isinstance(value, str):
            raise ValueError("Not valid type for email")
        if ("@", ".") in value:
            print("Email has at and dot")
        elif value.count("@") > 1:
            print("Valid email")
        else:
            print("Invalid email")