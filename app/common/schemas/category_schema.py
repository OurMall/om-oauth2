import datetime
from pydantic import Field
from beanie import Document, Indexed, Replace, after_event

class Category(Document):
    code_name: Indexed(str, unique=True) = Field(..., title="Code Name", description="Category code name")
    name: str = Field(..., title="Name", description="Category name")
    description: str = Field(..., title="Description", description="Category description")
    created_at: datetime.datetime | str = Field(datetime.datetime.now(), title="Created AT", description="Category creation date")
    updated_at: datetime.datetime | str = Field(datetime.datetime.now(), title="Updated AT", description="Category last updated")
    
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