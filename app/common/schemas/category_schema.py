import datetime
import pymongo
from beanie import Document, Indexed

class Category(Document):
    name: Indexed(str, index_type=pymongo.ASCENDING, unique=True)
    description: str
    created_at: datetime.datetime | str
    updated_at: datetime.datetime | str
    
    class Collection:
        name = "categories"
    
    class Settings:
        validate_on_save = True
        use_cache = True
        cache_expiration_time = datetime.timedelta(seconds=30)
        cache_capacity = 2