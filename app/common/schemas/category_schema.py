import datetime
import pymongo
from pydantic import Field
from beanie import Document, Indexed, PydanticObjectId, Replace, after_event

class Category(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    name: Indexed(str, index_type=pymongo.ASCENDING, unique=True)
    description: str
    created_at: datetime.datetime | str = Field(datetime.datetime.now())
    updated_at: datetime.datetime | str = Field(datetime.datetime.now())
    
    @after_event(Replace)
    def change_updated_at(self):
        self.updated_at = datetime.datetime.now()
    
    class Collection:
        name = "categories"
    
    class Settings:
        validate_on_save = True
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=30)
        cache_capacity = 2
    
    class Config:
        json_encoders = {
            id: lambda v: v.__str__()
        }