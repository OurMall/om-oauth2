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
    after_event
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
    picture: str
    website: str | None
    biography: str | None
    address: Address

class User(Document):
    name: str | None
    given_name: str
    family_name: str
    middle_name: str | None
    nickname: str | None
    preferred_username: str
    gender: Gender
    email: str = Indexed(str, index_type=pymongo.TEXT, unique=True)   # Unique 
    password: str | None
    phone_number: str
    profile: Profile
    birthdate: int | datetime.date
    zoneinfo: str
    locale: str
    email_verified: bool = Field(False)
    phone_number_verified: bool = Field(False)
    is_blocked: bool = Field(False)
    is_disabled: bool = Field(False)
    created_at: int | datetime.datetime
    updated_at: int | datetime.datetime
    permissions: list[Link[Permission]]
    groups: list[Link[Group]]
    clients: list[Link[Client]]
    #favorites: list[Link[Product]]
    
    @after_event(Insert)
    def join_fullname(self):
        self.name = " ".join([self.given_name, self.middle_name, self.family_name])
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "users"
    
    class Settings:
        validate_on_save = True # This validate field data types
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=60)
        cache_capacity = 3