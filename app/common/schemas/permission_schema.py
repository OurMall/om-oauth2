import pymongo
import datetime
from pydantic import Field
from beanie import Document, Indexed, after_event, Replace

class Permission(Document):
    code_name: Indexed(str, index_type=pymongo.ASCENDING, unique=True)
    name: str
    description: str | None
    created_at: int | datetime.datetime = Field(datetime.datetime.now())
    updated_at: int | datetime.datetime = Field(datetime.datetime.now())
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "permissions"