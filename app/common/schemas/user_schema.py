import enum
import datetime
import pymongo
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

class Gender(enum.Enum):
    MALE="male"
    FEMALE="female"
    OTHER="other"

class Profile(BaseSchema):
    picture: str | None
    website: str | None
    biography: str | None

class User(Document):
    name: str | None
    given_name: str
    family_name: str
    middle_name: str | None
    nickname: str | None
    preferred_username: str | None
    gender: Gender
    email: Indexed(str) # TODO:// change unique index
    password: str | None
    phone_number: str
    profile: Profile = Field(None)
    address: Address = Field(None)
    birthdate: datetime.datetime | str
    zoneinfo: str | None
    locale: str | None
    email_verified: bool = Field(False)
    phone_number_verified: bool = Field(False)
    is_blocked: bool = Field(False)
    is_disabled: bool = Field(False)
    created_at: int | datetime.datetime = Field(datetime.datetime.now())
    updated_at: int | datetime.datetime = Field(datetime.datetime.now())
    groups: list[Link[Group]] = Field([])
    permissions: list[Link[Permission]] = Field([]) # TODO:// pass to have to
    #clients: list[Link[Client]] = Field(None)
    #favorites: list[Link[Product]]
    
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