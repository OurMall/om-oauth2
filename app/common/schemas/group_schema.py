import pymongo
import datetime
from pydantic import Field
from beanie import Document, Link, Indexed, PydanticObjectId, after_event, Replace

from .permission_schema import Permission

class Group(Document):
    id: PydanticObjectId
    code_name: Indexed(str, index_type=pymongo.ASCENDING, unique=True)
    name: str
    description: str | None
    permissions: list[Link[Permission]]
    created_at: int | datetime.datetime = Field(datetime.datetime.now())
    updated_at: int | datetime.datetime = Field(datetime.datetime.now())
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "groups"
    
    class Config:
        json_encoders = {
            id: lambda v: v.__str__()
        }